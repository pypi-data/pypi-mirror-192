from .utils import search_all
from subprocess import run, PIPE
from urllib.parse import unquote
from lxml import html, etree
import time
import json
import os


def search(kw, page=1, **kwargs):
    return search_all(kw=kw, page=page, **kwargs)


def parse(raw):
    r = html.fromstring(raw.decode(errors="ignore"))
    r2 = r.xpath("//a[@href]/h3/..")
    if not r2:
        r2 = r.xpath("//a[@href]/div/h3/../..")
        if not r2:
            r2 = r.xpath("//a[@href]/div/div/h3/../../..")
    def tfa(e):
        return "".join(str(__) for __ in e if __)
    def tfb(e):
        e = str(e)
        if e.startswith("http"):
            return e
        e = e.split("/url?q=", 1)[-1].split("&url=", 1)[-1].split("&")[0]
        while True:
            try:
                f = unquote(e)
                if e == f:
                    return e
                e = f
            except:
                return e
    r = []
    for _ in r2:
        href = _.xpath("./@href")[0]
        if href.startswith("/search?"):
            continue
        r.append([tfa(_.xpath(".//h3//text()")), tfb(href)])
    return r
    # from .utils import NODEJS, JSONNET
    # rs = r.xpath("//script[contains(text(), 'JSON.parse') and contains(text(), '+1')]/text()")
    # r = max(rs, key=len)
    # r = r.split("JSON.parse")
    # if len(r) == 3 and "+1" in r[-1]:
    #     r = r[1]
    #     r = r.split("(function(){")
    #     r = r[-1]
    #     r = r.split("];")
    #     r = r[0]+"]"
    #     if NODEJS:
    #         var = r.split("var ")[1].split("=")[0]
    #         open("tmp.js", "wb").write((r+";console.log(JSON.stringify({}))".format(var)).encode())
    #         r = run(["node", "tmp.js"], stdout=PIPE, stderr=PIPE)
    #         os.remove("tmp.js")
    #         r = r.stdout.decode()
    #         return [json.loads(r), r2]
    # else:
    #     raise Exception("unknown script", "JSON.parse".join(r))


def process(parsed):
    return parsed
    # parsed, r2 = parsed
    # r = []
    # for i in range(0, len(parsed), 2):
    #     b = json.loads(parsed[i + 1])
    #     print(b)
    #     if isinstance(b, list) and len(b) == 6:
    #         if isinstance(b[0], str) and b[0].startswith("http"):
    #             r.append(b[0])
    # return r, r2


def get(**kwargs):
    for i in range(0, 5):
        try:
            return process(parse(search(**kwargs)))
        except Exception as e:
            if i == 4:
                raise e
            time.sleep(5)

