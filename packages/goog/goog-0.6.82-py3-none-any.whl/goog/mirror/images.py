from .utils import search_image, json_decode
from urllib.parse import unquote
from html import escape
from lxml import html, etree
import json
import time
import os
import re


def search(kw, page=1, **kwargs):
    return search_image(kw, page=page, **kwargs)


def parse_old(raw):
    r = html.fromstring(raw.decode())
    rs = [_ for _ in r.xpath("//script[contains(text(), 'AF_initDataCallback')]/text()")]
    if rs:
        r = max(rs, key=len)
        r = json_decode(str(r)[20:-2])
        r = json.loads(r)
        return r["data"][56][1][0][0][1][0]
    else:
        r2 = [etree.tostring(_, method="html") for _ in r.xpath("//*[@data-ou]")]
        if not r2:
            r2 = r.xpath("//td/a/div/img")
            if not r2:
                raise ValueError("raw is malformed, try to search and parse again")
            else:
                r = []
                for _ in r2:
                    img = _.xpath("./@src")[0]
                    href = _.xpath("./../../@href")[0]
                    if not href.startswith("http"):
                        href = href.split("/url?q=", 1)[-1].split("&url=", 1)[-1].split("&")[0]
                    while True:
                        try:
                            href2 = unquote(href)
                            if href==href2:
                                break
                            href = href2
                        except:
                            pass
                    title = _.xpath("./../../../../../tr[2]/td/a//span/text()")
                    title = [_ for _ in title if _.strip()][0]
                    r.append("<div data-pt=\"{}\" data-ru=\"{}\" data-ou=\"{}\">".format(
                        escape(str(title)),
                        escape(str(href)),
                        escape(str(img)),
                    ).encode())
        else:
            r = r2
        return r


def process_old(parsed):
    r = []
    if isinstance(parsed[0], bytes):
        for _ in parsed:
            _ = html.fromstring(_.decode())
            r.append([
                _.xpath("//div/@data-pt")[0],
                _.xpath("//div/@data-ru")[0],
                _.xpath("//div/@data-ou")[0],
            ])
    else:
        for i, _ in enumerate(parsed):
            _ = list(_[0][0].values())[0]
            imgs = []
            urls = []
            titles = []
            if not _[1]:
                continue
            for __ in _[1]:
                if isinstance(__, list):
                    imgs.append(__)
                elif isinstance(__, dict):
                    for ___ in __.values():
                        for ____ in ___:
                            if isinstance(____, str):
                                if ____.startswith("http"):
                                    urls.append(____)
                                elif urls:
                                    titles.append(____)
            url = urls[0]
            img = imgs[-1][0]
            title = titles[0]
            r.append([
                title,
                url,
                img
            ])
    return r


def parse(raw):
    r = re.search(rb"(\[\[.*?\]\])\n", raw)[1]
    r = json.loads(json_decode(r.decode()))
    r = json.loads(json_decode(r[0][2]))
    return r[56][1][0][0][1][0]


def process(parsed):
    return process_old(parsed)


def get(**kwargs):
    for i in range(0, 5):
        try:
            return process(parse(search(**kwargs)))
        except Exception as e:
            if i == 4:
                raise e
            time.sleep(5)

