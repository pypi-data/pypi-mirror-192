import datetime
import mimetypes
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.conf import arglist_to_dict
from tqdm import tqdm
from warcio.statusandheaders import StatusAndHeaders
from warcio.warcwriter import WARCWriter

from .io import archive_files
from .spider import CrauSpider
from .utils import HTTP_STATUS_CODES, WarcReader, get_urls_from_file
from .version import __version__


def run_command(command):
    print(f"*** Running command: {command}")
    return subprocess.call(shlex.split(command))


def load_settings(ctx, param, value):
    settings = {
        "HTTPCACHE_ENABLED": False,
        "LOG_LEVEL": "CRITICAL",
        "STATS_CLASS": "crau.utils.StdoutStatsCollector",
        "USER_AGENT": f"crau {__version__}",
    }
    settings.update(arglist_to_dict(value))
    return settings


@click.group()
@click.version_option(version=__version__, prog_name="crau")
def cli():
    pass


@cli.command("list", help="List URIs of response records stored in a WARC file")
@click.argument("warc_filename")
def list_uris(warc_filename):
    warc = WarcReader(warc_filename)
    for record in warc:
        if record.rec_type == "response":
            click.echo(record.rec_headers.get_header("WARC-Target-URI"))


@cli.command("extract", help="Extract URL content from archive")
@click.option("--chunk-size", default=512 * 1024)
@click.argument("warc_filename")
@click.argument("uri")
@click.argument("output")
def extract_uri(chunk_size, warc_filename, uri, output):
    warc = WarcReader(warc_filename)
    stream = warc.get_response(uri).content_stream()

    if output == "-":
        data = stream.read(chunk_size)
        while data != b"":
            sys.stdout.buffer.write(data)
            data = stream.read(chunk_size)
    else:
        with open(output, mode="wb") as fobj:
            data = stream.read(chunk_size)
            while data != b"":
                fobj.write(data)
                data = stream.read(chunk_size)


@cli.command("archive", help="Archive a list of URLs to a WARC file")
@click.argument("warc_filename")
@click.option("--input-filename", "-i")
@click.option("--input-encoding", default="utf-8")
@click.option("--cache", is_flag=True)
@click.option("--max-depth", default=1)
@click.option("--allowed-uris", multiple=True, default=[])
@click.option("--autothrottle", is_flag=True)
@click.option("--log-level", required=False)
@click.option("--user-agent", required=False)
@click.option("--settings", "-s", multiple=True, default=[], callback=load_settings)
@click.argument("URLs", nargs=-1, required=False)
def archive(
    warc_filename,
    input_filename,
    input_encoding,
    cache,
    max_depth,
    allowed_uris,
    autothrottle,
    log_level,
    settings,
    user_agent,
    urls,
):

    if not input_filename and not urls:
        click.echo(
            "ERROR: at least one URL must be provided (or a file containing one per line).",
            err=True,
        )
        exit(1)

    if input_filename:
        if not Path(input_filename).exists():
            click.echo(f"ERROR: filename {input_filename} does not exist.", err=True)
            exit(2)
        urls = get_urls_from_file(input_filename, encoding=input_encoding)

    if cache:
        settings["HTTPCACHE_ENABLED"] = True

    if log_level:
        settings["LOG_LEVEL"] = log_level

    if user_agent:
        settings["USER_AGENT"] = user_agent

    if autothrottle:
        settings.update(
            {
                "AUTOTHROTTLE_ENABLED": True,
                "AUTOTHROTTLE_DEBUG": True,
            }
        )

    process = CrawlerProcess(settings=settings)
    process.crawl(
        CrauSpider,
        warc_filename=warc_filename,
        urls=urls,
        max_depth=max_depth,
        allowed_uris=allowed_uris,
    )
    process.start()
    # TODO: if there's an error, print it


@cli.command("play", help="Run a backend playing your archive")
@click.option("-p", "--port", default=8000)
@click.option("-b", "--bind", default="127.0.0.1")
@click.argument("warc_filename")
def play(warc_filename, port, bind):
    filename = Path(warc_filename)
    if not filename.exists():
        click.echo(f"ERROR: filename {warc_filename} does not exist.", err=True)
        exit(2)

    full_filename = filename.absolute()
    collection_name = filename.name.split(".")[0]
    temp_dir = tempfile.mkdtemp()
    old_cwd = os.getcwd()

    os.chdir(temp_dir)
    run_command(f'wb-manager init "{collection_name}"')
    run_command(f'wb-manager add "{collection_name}" "{full_filename}"')
    run_command(f"wayback -p {port} -b {bind}")
    shutil.rmtree(temp_dir)
    os.chdir(old_cwd)


@cli.command("pack", help="Pack one or more files into a WARC")
@click.argument("start_url")
@click.argument("path_or_archive")
@click.argument("warc_filename")
@click.option("--inner-directory")
def pack(start_url, path_or_archive, warc_filename, inner_directory=None):
    # TODO: move the packing code to another module
    if not start_url.endswith("/"):
        start_url = start_url + "/"
    path_or_archive = Path(path_or_archive)
    warc_filename = Path(warc_filename)
    if not warc_filename.parent.exists():
        warc_filename.parent.mkdir(parents=True)
    inner_directory = Path(inner_directory) if inner_directory is not None else None

    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    tz = datetime.timezone(offset=-datetime.timedelta(seconds=offset))
    with warc_filename.open(mode="wb") as warc_fobj:
        writer = WARCWriter(warc_fobj, gzip=warc_filename.suffixes[-1].lower() == ".gz")
        for file_info in tqdm(
            archive_files(path_or_archive, inner_directory), "Packing files"
        ):
            if file_info.is_dir:
                continue
            warc_headers_dict = {
                "WARC-Date": file_info.created_at.replace(tzinfo=tz).strftime(
                    "%Y-%m-%dT%H:%M:%S%z"
                ),
            }
            url = urljoin(start_url, str(file_info.path))
            path = url[url.find("/", len(urlparse(url).scheme) + 3) :]
            url = url[: len(url) - len(path)] + quote(path)
            http_headers = StatusAndHeaders(
                f"GET {quote(path)} HTTP/1.1", [], is_http_request=True
            )
            writer.write_record(
                writer.create_warc_record(
                    url,
                    "request",
                    http_headers=http_headers,
                    warc_headers_dict=warc_headers_dict,
                )
            )

            status_code = 200
            header_list = [("Content-Length", str(file_info.size))]
            content_type, _ = mimetypes.guess_type(path)
            if content_type is not None:
                header_list.append(("Content-Type", content_type))
            status_title = HTTP_STATUS_CODES.get(status_code, "Unknown")
            http_headers = StatusAndHeaders(
                f"{status_code} {status_title}",
                header_list,
                protocol="HTTP/1.1",
                is_http_request=False,
            )
            writer.write_record(
                writer.create_warc_record(
                    url,
                    "response",
                    payload=file_info.fobj,
                    http_headers=http_headers,
                    warc_headers_dict=warc_headers_dict,
                )
            )
