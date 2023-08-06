import logging
import re
from collections import namedtuple
from urllib.parse import urljoin

from scrapy import Request, Spider, signals
from scrapy.utils.request import request_fingerprint
from warcio.warcwriter import WARCWriter

from .utils import resource_matches_base_url, write_warc_request_response

Resource = namedtuple("Resource", ["name", "type", "link_type", "content"])
REGEXP_CSS_URL = re.compile(r"""url\(['"]?(.*?)['"]?\)""")

Extractor = namedtuple("Extractor", ["name", "type", "link_type", "xpath"])
EXTRACTORS = [
    # Media (images, video etc.)
    Extractor(name="media", type="link", link_type="dependency", xpath="//img/@src"),
    Extractor(name="media", type="link", link_type="dependency", xpath="//audio/@src"),
    Extractor(name="media", type="link", link_type="dependency", xpath="//video/@src"),
    Extractor(name="media", type="link", link_type="dependency", xpath="//source/@src"),
    Extractor(name="media", type="link", link_type="dependency", xpath="//embed/@src"),
    Extractor(
        name="media", type="link", link_type="dependency", xpath="//object/@data"
    ),
    # CSS
    Extractor(
        name="css",
        type="link",
        link_type="dependency",
        xpath="//link[@rel = 'stylesheet']/@href",
    ),
    Extractor(name="css", type="code", link_type="dependency", xpath="//style/text()"),
    Extractor(name="css", type="code", link_type="dependency", xpath="//*/@style"),
    # JavaScript
    Extractor(name="js", type="link", link_type="dependency", xpath="//script/@src"),
    Extractor(name="js", type="code", link_type="dependency", xpath="//script/text()"),
    # TODO: add "javascript:XXX" on //a/@href etc.
    # TODO: add inline JS (onload, onchange, onclick etc.)
    # Internal/external links and iframes
    # TODO: iframe sources must be considered as if they were the same as the
    # current page being archived (same depth, get all dependencies etc.).
    Extractor(name="other", type="link", link_type="anchor", xpath="//iframe/@src"),
    Extractor(name="other", type="link", link_type="anchor", xpath="//a/@href"),
    Extractor(name="other", type="link", link_type="anchor", xpath="//area/@href"),
    Extractor(
        name="other",
        type="link",
        link_type="anchor",
        xpath="//link[not(@rel = 'stylesheet')]/@href",
    ),
    # TODO: link rel=icon should be considered a dependency (what about other
    # link rel=xxx?)
    # TODO: add all other "//link/@href"
]


def extract_resources(response):
    for extractor in EXTRACTORS:
        for content in response.xpath(extractor.xpath).extract():
            yield Resource(
                name=extractor.name,
                type=extractor.type,
                link_type=extractor.link_type,
                content=content,
            )


class CrauSpider(Spider):

    name = "crawler-spider"
    custom_settings = {
        "CONCURRENT_REQUESTS": 256,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
        "DNSCACHE_ENABLED": True,
        "DNSCACHE_SIZE": 500000,
        "DNS_TIMEOUT": 5,
        "DOWNLOAD_MAXSIZE": 5 * 1024 * 1024,
        "DOWNLOAD_TIMEOUT": 15,
        "REACTOR_THREADPOOL_MAXSIZE": 40,
        "REDIRECT_ENABLED": False,
        "SCHEDULER_PRIORITY_QUEUE": "scrapy.pqueues.DownloaderAwarePriorityQueue",
        "SPIDER_MIDDLEWARES_BASE": {
            "scrapy.spidermiddlewares.httperror.HttpErrorMiddleware": 50,
            "scrapy.spidermiddlewares.offsite.OffsiteMiddleware": 500,
            "scrapy.spidermiddlewares.referer.RefererMiddleware": 700,
            "scrapy.spidermiddlewares.urllength.UrlLengthMiddleware": 800,
        },
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def __init__(self, warc_filename, urls, max_depth=1, allowed_uris=None):
        super().__init__()
        self.max_depth = int(max_depth)
        self.warc_filename = warc_filename
        self.urls = urls
        self._request_history = set()
        self.warc_fobj = None
        self.warc_writer = None
        self.allowed_uris = allowed_uris if allowed_uris else []

    def spider_closed(self, spider):
        if self.warc_fobj is not None:
            self.warc_fobj.close()

    def make_request(self, request_class=Request, *args, **kwargs):
        """Method to create requests and implements a custom dedup filter"""

        kwargs["dont_filter"] = kwargs.get("dont_filter", True)
        kwargs["errback"] = kwargs.get("errback", self.parse_request_error)

        meta = kwargs.get("meta", {})
        meta["handle_httpstatus_all"] = meta.get("handle_httpstatus_all", True)
        meta["dont_redirect"] = meta.get("dont_redirect", True)
        kwargs["meta"] = meta

        request = request_class(*args, **kwargs)
        if "#" in request.url:
            request = request.replace(url=request.url[: request.url.find("#")])

        # This `if` filters duplicated requests - we don't use scrapy's dedup
        # filter because it has a bug, which filters out requests in undesired
        # cases <https://github.com/scrapy/scrapy/issues/1225>.
        # TODO: check if this dedup filter does not have the same problem
        # scrapy have (the problem is related to canonicalize request url).
        request_hash = request_fingerprint(request)
        # TODO: may move this in-memory set to a temp file since the number of
        # requests can be pretty large.
        if request_hash in self._request_history:
            return None
        else:
            self._request_history.add(request_hash)
            return request

    def write_warc(self, response):
        # TODO: transform this method into `write_response` so we can have
        # other response writers than WARC (CSV, for example - would be great
        # if we can add specific parsers to save HTML's title and text into
        # CSV, for example).
        write_warc_request_response(self.warc_writer, response)

    def start_requests(self):
        """Start requests with depth = 0

        depth will be 0 for all primary URLs and all requisites (CSS, Images
        and JS) of these URLs. For links found on these URLs, depth will be
        incremented, and so on.
        """
        self.warc_fobj = open(self.warc_filename, mode="wb")
        self.warc_writer = WARCWriter(self.warc_fobj, gzip=True)

        for url in self.urls:
            yield self.make_request(
                url=url, meta={"depth": 0, "main_url": url}, callback=self.parse
            )

    def parse(self, response):
        main_url = response.request.url
        # TODO: what if response.request.url != response.url?
        current_depth = response.request.meta["depth"]
        next_depth = current_depth + 1

        content_type = response.headers.get("Content-Type", b"").decode(
            "ascii"
        )  # TODO: decode properly
        if content_type and content_type.split(";")[0].lower() != "text/html":
            logging.debug(
                f"[{current_depth}] Content-Type not found for {main_url}, parsing as media"
            )
            yield self.parse_media(response)
            return

        logging.debug(f"[{current_depth}] Saving HTML {response.request.url}")
        self.write_warc(response)

        redirect_url = None
        if 300 <= response.status <= 399 and "Location" in response.headers:
            redirect_url = urljoin(
                response.request.url,
                response.headers["Location"].decode("ascii"),  # TODO: decode properly
            )

        for resource in extract_resources(response):
            if resource.type == "link":
                # TODO: handle "//" URLs correctly
                absolute_url = urljoin(main_url, resource.content)
                depth = None
                if resource.link_type == "dependency":
                    depth = current_depth
                elif resource.link_type == "anchor":
                    depth = next_depth
                for request in self.collect_link(
                    main_url, resource.name, absolute_url, depth
                ):
                    if request is None or (
                        redirect_url is not None and redirect_url == request.url
                    ):
                        continue
                    elif (
                        self.allowed_uris
                        and resource.link_type == "anchor"
                        and not resource_matches_base_url(
                            absolute_url, self.allowed_uris
                        )
                    ):
                        logging.info(f"Different domain. Skipping {absolute_url}.")
                        continue
                    yield request

            elif resource.type == "code":
                for request in self.collect_code(
                    main_url, resource.name, resource.content, current_depth
                ):
                    if request is None:
                        continue
                    yield request

        if redirect_url is not None:
            # TODO: how to deal with redirect loops?
            logging.debug(f"[{current_depth}] Redirecting to {redirect_url}")
            yield self.make_request(
                url=redirect_url,
                meta={"depth": current_depth, "main_url": main_url},
                callback=self.parse,
            )

    def parse_request_error(self, failure):
        pass
        # TODO: should we do something with this failure?

    def parse_css(self, response):
        meta = response.request.meta

        for request in self.collect_code(
            response.request.url, "css", response.body, meta["depth"]
        ):
            if request is None:
                continue
            yield request

        logging.debug(f"Saving CSS {response.request.url}")
        self.write_warc(response)

    def parse_js(self, response):
        meta = response.request.meta

        for request in self.collect_code(
            response.request.url, "js", response.body, meta["depth"]
        ):
            if request is None:
                continue
            yield request

        logging.debug(f"Saving JS {response.request.url}")
        self.write_warc(response)

    def parse_media(self, response):
        logging.debug(f"Saving MEDIA {response.request.url}")
        self.write_warc(response)

    def collect_link(self, main_url, link_type, url, depth):
        if depth > self.max_depth:
            logging.debug(
                f"[{depth}] IGNORING (depth exceeded) get link {link_type} {url}"
            )
            return []
        elif not url.startswith("http"):
            logging.debug(f"[{depth}] IGNORING (not HTTP) get link {link_type} {url}")
            return []

        if link_type == "media":
            return [
                self.make_request(
                    url=url,
                    callback=self.parse_media,
                    meta={"depth": depth, "main_url": main_url},
                )
            ]
        elif link_type == "css":
            return [
                self.make_request(
                    url=url,
                    callback=self.parse_css,
                    meta={"depth": depth, "main_url": main_url},
                )
            ]
        elif link_type == "js":
            return [
                self.make_request(
                    url=url,
                    callback=self.parse_js,
                    meta={"depth": depth, "main_url": main_url},
                )
            ]
        elif link_type == "other":
            return [
                self.make_request(
                    url=url,
                    callback=self.parse,
                    meta={"depth": depth, "main_url": main_url},
                )
            ]
        else:
            return [
                self.make_request(
                    url=url,
                    callback=self.parse,
                    meta={"depth": depth, "main_url": main_url},
                )
            ]

    def collect_code(self, main_url, code_type, code, depth):
        if depth > self.max_depth:
            logging.debug(
                f"[{depth}] IGNORING (depth exceeded) getting dependencies for {code_type}"
            )
            return []
        elif code_type == "css":
            if isinstance(code, bytes):
                code = code.decode("utf-8")  # TODO: decode properly
            requests = []
            for result in REGEXP_CSS_URL.findall(code):
                url = urljoin(main_url, result)
                if url.startswith("data:"):
                    continue
                requests.append(
                    self.make_request(
                        url=url,
                        callback=self.parse_media,
                        meta={"depth": depth, "main_url": main_url},
                    )
                )
            return requests
        elif code_type == "js":
            # TODO: extract other references from JS code
            return []
        else:
            logging.info(f"[{depth}] [TODO] PARSE CODE {code_type} {code}")
            return []
            # TODO: change
