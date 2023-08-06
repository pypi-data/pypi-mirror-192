from cloudscraper import create_scraper, User_Agent
from subprocess import run, PIPE
import urllib3
from html import escape, unescape
from urllib.parse import quote, unquote
from lxml import html, etree
from datetime import datetime
import requests
import re
import os
import json
from shutil import which
import random
import chardet


urllib3.disable_warnings()
JSONNET = True
NODEJS = True
if not which("node"):
    NODEJS = False
    try:
        import _jsonnet
    except:
        JSONNET = False
if not NODEJS and not JSONNET:
    raise ImportError("js object decoder is required (node.js or jsonnet)")


mirrors = [
    # ["https", "note.cm", 0],
    ["https", "dhobi.win", 0],
    ["https", "goo.xbzxs.org", 0],
    # ["https", "xn--flw351e.vercel.app", 0],
    ["https", "google.uitsrt.top", 0],

    ["https", "xgoogle.xyz", 1],
    ["https", "shitu.paodekuaiweixinqun.com", 1],

    ["http", "173.242.117.245:88", 0],
    ["http", "117.120.10.100", 0],
    ["http", "34.92.52.42", 0],
    ["http", "140.128.197.26", 0],
    ["https", "alexnocella.com", 0],
    ["http", "45.62.121.69", 0],
    ["http", "43.132.187.107", 0],
    ["http", "192.118.67.139:82", 0],
    ["https", "g.xdog.nl", 0],
    ["https", "gg.gaioo.com", 0],
    # ["http", "map1.cnmaps.cn", 0],
    ["http", "134.73.87.2", 0],
    ["https", "map1.cnmaps.cn", 0],
    ["https", "gogo.crackcreed.com", 0],
    ["http", "8.210.104.175:8889", 0],
    ["http", "google.aabaao.com", 0],
    ["http", "117.120.10.81", 0],
    ["http", "82.220.37.174:7777", 0],
    ["http", "157.52.137.66", 0],
    ["https", "g.kaicao.dev", 0],
    ["http", "185.239.71.52:880", 0],
    ["https", "g.ys6.club", 0],
    ["http", "nat.shenjl.club", 0],
    ["http", "101.32.220.92:7777", 0],
    ["https", "xbaa.secems.net", 0],
    ["http", "a.abcellsci.com", 0],
    ["https", "gg.bunny.icu", 0],
    ["http", "133.35.116.80:8080", 0],
    ["http", "193.169.195.20:8080", 0],
    ["http", "g.shopizdw.top", 0],
    ["https", "www-google-com.o365.bot.skyfencenet.com", 0],
    ["http", "185.11.145.52:81", 0],
    ["https", "g.jinergy.com", 0],
    ["https", "bypassproxyforartworksbyconstantdullaart.arthost.nl", 0],
    ["https", "g.andytimes.xyz", 0],
    ["http", "119.28.108.82:8089", 0],
    ["http", "104.243.28.195:8020", 0],
    ["http", "search.fatwo.cn", 0],
    ["http", "185.61.137.186:81", 0],
    ["http", "g.52hua.com", 0],
    ["http", "104.148.62.226", 0],
    ["http", "96.57.226.10", 0],
    ["http", "35.197.71.34", 0],
    ["http", "13.41.139.21:8000", 0],
    ["http", "178.157.58.200", 0],
    ["http", "192.118.67.120:81", 0],
    ["http", "apps.minfun.net", 0],
    ["http", "o.poetpalace.org", 0],
    ["http", "164.88.197.81", 0],
    ["http", "203.137.163.53:8080", 0],
    ["http", "16.162.44.118", 0],
    ["http", "144.168.56.90:88", 0],
    ["https", "google.xuzp.net", 0],
    ["http", "52.77.204.119", 0],
    ["https", "s.imix.im", 0],
    ["https", "g.jinh.ltd", 0],
    ["http", "g.tou.mobi", 0],
    ["http", "xg.gvrcraft.com:8008", 0],
    ["http", "193.123.224.188", 0],
    ["https", "ff.moose.eu.org", 0],
    ["https", "gg.artwc.com", 0],
    ["http", "104.160.41.254:1025", 0],

    # ["http", "47.243.6.6:10001", 0],
    ["https", "119.8.96.123", 0],
    ["https", "jsapi.usthk.cn", 0],
    ["http", "63.210.148.67", 0],
    # ["https", "google.1qi777.com", 0],
    ["https", "94.74.125.6", 0],
    # ["http", "34.205.16.120", 0],
    ["https", "8.214.34.95", 0],
    ["https", "176.32.35.106", 0],
    ["https", "66.42.68.250", 0],
    ["https", "184.73.64.147", 0],
    ["http", "cabinet.diaana.ch", 0],
    ["http", "google.huangshenshi.com", 0],
    # ["http", "94.74.125.6", 0],
    ["https", "8.210.245.52", 0],
    ["https", "47.242.124.252", 0],
    ["http", "94.74.110.58", 0],
    ["http", "167.179.80.165:9876", 0],
    ["https", "216.24.186.84", 0],
    ["https", "158.101.132.84", 0],
    ["https", "129.226.49.38", 0],
    ["http", "google.imfun.tk", 0],
    ["https", "47.87.215.24", 0],
    ["https", "118.193.37.85", 0],
    ["https", "23.106.131.211", 0],
    ["http", "6cmap.com", 0],
    ["http", "47.75.165.14", 0],
    ["http", "68.71.130.102:84", 0],
    ["https", "g.crazydan.cn", 0],
    # ["https", "47.243.6.6", 0],
    ["https", "13.114.115.117", 0],
    ["https", "172.96.206.8:8443", 0],
    ["http", "68.71.130.100:84", 0],
    ["https", "119.28.2.156", 0],
    # ["http", "47.74.3.55", 0],
    ["http", "45.137.190.150:81", 0],
    ["http", "144.34.165.45", 0],
    # ["http", "trueloveshop.cn:8888", 0],
    ["http", "68.71.130.98:84", 0],
    ["https", "jwadef.secems.net", 0],
    ["http", "144.24.162.79:8089", 0],
    ["https", "23.226.227.21:444", 0],
    ["http", "47.90.246.146:30001", 0],
    ["https", "43.128.106.224", 0],
    # ["http", "47.88.91.126:22222", 0], # offline
    ["http", "172.104.96.184", 0],
    # ["http", "13.114.115.117", 0],
    ["https", "google.linzhehao.cn", 0],
    ["http", "67.207.76.250:8880", 0],
    ["http", "google.lanzhe.org", 0],
    ["https", "47.74.3.55", 0],
    ["https", "sksjd.vaxilu.com", 0],
    ["http", "159.138.155.105:9001", 0],
    ["http", "199.19.108.146", 0],
    # ["https", "47.242.119.0", 0], # offline
    # ["http", "43.153.4.89:8888", 0],
    # ["http", "74.211.96.123", 0], # offline
    ["https", "espduo.net", 0],
    # ["https", "hamradio.ml", 0],
    # ["https", "172.96.195.39", 0],
    # ["http", "www.lanchx.cn", 0], # offline
    # ["https", "apis.g.crazydan.cn", 0],
    # ["https", "tokyo4.wardao.xyz", 0], # offline
    # ["https", "test1.bigjuan.xyz", 0], # offline
    # ["https", "23.234.225.112", 0], # offline
    # ["http", "35.201.180.233:8080", 0], # offline
    # ["https", "ulovem.eu.org", 0],
    # ["http", "gg.jasonmm.xyz", 0], # offline
    ["http", "176.113.71.49:8080", 0],
    # ["http", "35.244.255.226", 0],
    ["http", "195.15.238.230", 0],
    ["https", "google.774.gs", 0],
    ["https", "www.altdatamap.com", 0],
    ["http", "119.28.42.163:8080", 0],
    ["https", "43.156.29.174", 0],
    # ["http", "54.190.15.132", 0], # offline
    # ["http", "google.fenliproxy.top", 0],
    # ["http", "207.148.99.17:8080", 0], # offline
    ["https", "g2.cother.org", 0],
    ["http", "34.222.8.158", 0],
    # ["http", "13.59.176.88:8081", 0], # offline
    ["https", "193.161.193.77", 0],
    # ["https", "wardao.xyz", 0], # offline
    ["http", "13.76.152.212:81", 0],
    # ["http", "wentidayi.com:8888", 0],
    # ["http", "g.19688.cn", 0],
    ["http", "47.254.85.86", 0],
    ["http", "18.222.202.27", 0],
    # ["http", "18.191.48.246:8081", 0], # offline
    ["https", "47.243.118.247", 0],
    # ["https", "del.wardao.xyz", 0], # offline
    # ["http", "94.74.111.55", 0], # offline
    # ["https", "47.74.133.147", 0], # offline
    ["http", "linebot.ycwww.dev", 0],
    ["https", "35.230.234.249", 0],
    # ["https", "104.225.238.101", 0], # offline
    # ["http", "8.12.17.139", 0], # offline
    # ["https", "71.232.17.60", 0], # offline
    ["https", "alhena.com.cn", 0],
    # ["https", "www.joautum.top", 0],
    ["https", "www.espduo.net", 0],
    ["https", "190.95.221.138", 0],
    # ["http", "99.dony.wang", 0],
    ["https", "g.yyvpn.net", 0],
    ["https", "g.rbq.ac.cn", 0],
    # ["http", "129.226.60.168:8888", 0], # offline
    # ["http", "89.208.255.77", 0],
    ["https", "45.141.136.197:8444", 0],
    # ["https", "210.203.218.222", 0], # offline
    # ["http", "195.93.173.18", 0], # offline
    ["https", "63.223.84.246:8444", 0],
    # ["https", "13.58.149.127", 0], # offline
    # ["https", "blog.alvarny.com", 0], # offline
    # ["https", "87.120.8.71", 0],
    ["http", "favicons.tempest.com", 0],
    # ["https", "g.zzygx.ml", 0],
    ["http", "43.129.70.227", 0],
    # ["https", "4.246.158.129", 0], # offline
    ["https", "o00p.vip:8444", 0],
    ["https", "g.lovingfrank.net", 0],
    # ["https", "144.34.164.174:444", 0], # offline
    # ["http", "146.56.180.1", 0],
    # ["https", "47.254.19.126", 0], # broken
    ["https", "144.168.61.187:8443", 0],
    # ["https", "pem.app", 0],
    # ["https", "217.22.30.127", 0], # offline
    # ["https", "3.15.65.194", 0], # offline
    # ["https", "151.139.109.74", 0], # offline
    # ["http", "87.237.55.82", 0],
    # ["https", "151.139.111.247", 0], # offline
    ["https", "172.96.219.170", 0],
    ["https", "64.27.27.49", 0],
    ["https", "63.223.84.245:8444", 0],
    ["https", "google.oracleblog.org", 0],
    # ["https", "a2.520guge.com:8444", 0], # offline
    # ["http", "52.79.84.19", 0], # offline
    # ["https", "89.208.255.77", 0],
    # ["https", "47.52.155.64", 0],
    ["https", "45.142.158.67:8444", 0],
    ["https", "upkube.cn:8443", 0],
    ["https", "96.43.88.62:8444", 0],
    # ["https", "151.139.105.108", 0], # offline
    ["http", "47.56.186.219", 0],
    # ["https", "kr.520guge.com:8444", 0], # offline
    ["https", "iseekyou.top", 0],
    # ["https", "v2.520guge.com:8444", 0], # offline
    ["http", "gooogie.ru", 0],
    # ["https", "47.52.73.151", 0], # offline
    ["https", "www.iseekyou.top", 0],
    # ["http", "fdl.wuzhizhuan.com", 0],
    # ["https", "huforols.space", 0],
    ["http", "3.14.126.143", 0],
    # ["http", "78.141.199.53", 0], # broken
    # ["https", "xyt3.520guge.com:8444", 0], # offline
    ["https", "173.82.110.222:8444", 0],
    ["http", "119.28.14.218", 0],
    ["http", "43.133.38.181", 0],
    ["https", "cmapc.cn", 0],
    # ["https", "a1.520guge.com:8444", 0], # offline
    # ["http", "15.205.122.194:8081", 0], # offline
    # ["http", "ww.long-photo.net", 0],
    ["https", "144.202.69.73", 0],
]
#秋葉原冥途戰爭
whitelist = [_[1] for _ in mirrors if _[2]]
mirrors = [_[:2] for _ in mirrors]
ext_redirect = [
    "/extdomains/",
]
'''
https://blog.csdn.net/lwdfzr/article/details/124805045


plaintext = "秋葉原冥途戰爭".encode()
iv = b"badassbadassbada"
ciphertext = AESCipherCBCnoHASHwoIV(key=iv, iv=iv).encrypt(plaintext)
from base64 import b64decode
print(plaintext, b64decode(ciphertext).hex())
'''
TBM = {
    "All": "",
    "Applications": "tbm=app",
    "Blogs": "tbm=blg",
    "Books": "tbm=bks",
    "Discussions": "tbm=dsc",
    "Images": "tbm=isch",
    "News": "tbm=nws",
    "Patents": "tbm=pts",
    "Places": "tbm=plcs",
    "Recipes": "tbm=rcp",
    "Shopping": "tbm=shop",
    "Videos": "tbm=vid",
}
google_domain = "google.com.hk"
search_url = "https://{}/search?q={{}}".format(google_domain)


def s(cloudscraper=True):
    if cloudscraper:
        while True:
            try:
                s = create_scraper(browser={"mobile": False})
                return s
            except:
                continue
    return requests.Session()


def random_mirror(k=None):
    if k is None:
        return random.SystemRandom().choice(mirrors)
    return mirrors[k]


def transform(url, k):
    proto, domain = random_mirror(k)
    url = url.split("/")
    url[0] = proto+":"
    url[2] = domain
    print("/".join(url))
    return "/".join(url)


def detect_encoding(c):
    try:
        c.decode()
        return c
    except:
        pass
    try:
        return c.decode("gbk").encode()
    except:
        pass
    try:
        return c.decode("big5").encode()
    except:
        pass
    try:
        return c.decode("latin1").encode()
    except:
        pass
    r = chardet.detect(c)
    enc = r["encoding"]
    if enc[:2] == "gb":
        enc = "gbk"
    return c.decode(enc, errors="replace").encode()


def json_decode(w):
    if NODEJS:
        open("tmp.js", "wb").write(("console.log(JSON.stringify(" + w + "));").encode())
        r = run("node {}".format(os.getcwd(), "tmp.js"), shell=True, stderr=PIPE, stdout=PIPE).stdout.decode()
        os.remove("tmp.js")
        return r
    elif JSONNET:
        import _jsonnet
        r = _jsonnet.evaluate_snippet("snippet", w)
        return r


def get(url, k, page=1):
    url = transform(url, k)
    d = url.split("/")[2]
    try:
        r = s(True).get(url, timeout=10)
    except:
        r = s(False).get(url, timeout=10, verify=False)
    c = r.content
    c = detect_encoding(c)
    if d in whitelist:
        c = c.replace(d.encode(), google_domain.encode())
        for _ in ext_redirect:
            c = c.replace((google_domain+_).encode(), b"")
    r._content = c
    return r


def get_raw(url, k, page=1):
    return get(url, k).content


def post(url, data, k):
    url = transform(url, k)
    d = url.split("/")[2]
    try:
        r = s(True).post(url, timeout=10, data=data)
    except:
        r = s(False).post(url, timeout=10, data=data, verify=False)
    c = r.content
    c = detect_encoding(c)
    if d in whitelist:
        c = c.replace(d.encode(), google_domain.encode())
        for _ in ext_redirect:
            c = c.replace((google_domain+_).encode(), b"")
    r._content = c
    return r


def post_raw(url, data, k):
    return post(url, data, k).content


def search(kw, cat="All", page=1, raw=True, k=None, **kwargs):
    # import time
    if cat not in TBM:
        raise KeyError(cat)
    url = search_url.format(kw)
    if cat in [
        "All",
    ]:
        url += "&start={}".format(10*(page-1))
    cat = TBM[cat]
    if cat:
        url += "&{}".format(cat)
    # st = time.time()
    if raw:
        r = get_raw(url, k, page=page)
    else:
        r = get(url, k, page=page)
    # print("_search", time.time()-st)
    return r


def search_all(kw, page=1, raw=True, k=None, **kwargs):
    cat = "All"
    return search(kw, cat=cat, page=page, raw=raw, k=k, **kwargs)


def search_image(kw, page=1, raw=True, k=None, r=None, **kwargs):
    cat = "Images"
    r = r or search(kw, cat=cat, page=1, raw=False, k=k, **kwargs)
    url = r.request.url
    c = r.content
    r = html.fromstring(c.decode())
    rs = [_ for _ in r.xpath("//script[contains(text(), 'AF_initDataCallback')]/text()")]
    if not rs:
        return c
    r = re.search(rb"AF_dataServiceRequests ?=(.*?);", c)[1].strip()
    # r = detect_encoding(r)
    AF_dataServiceRequests = json.loads(json_decode(r.decode()))
    request_ds1 = AF_dataServiceRequests["ds:1"]["request"][28]
    # print(request_ds1)
    r = max(rs, key=len)
    r = json_decode(str(r)[20:-2])
    AF_initDataCallback = json.loads(r)
    data = AF_initDataCallback["data"]
    data = list(data[56][1][0][0][0][0].values())[0][12]
    data1 = data[11]
    data2 = [None]+data[16][3:]
    # print(data1, data2)
    WIZ_global_data = re.search(rb"window.WIZ_global_data(.*?);", c)[1].split(b"=", 1)[-1].strip()
    # WIZ_global_data = detect_encoding(WIZ_global_data)
    # print(WIZ_global_data.decode())
    WIZ_global_data = json.loads(json_decode(WIZ_global_data.decode()))
    sid = WIZ_global_data["FdrFJe"]
    bl = WIZ_global_data["cfb2h"]
    hl = WIZ_global_data["GWsdKe"]
    _reqid = 1 + (3600 * datetime.now().hour + 60 * datetime.now().minute + datetime.now().second) + 100000 * page
    # print(sid, bl, _reqid)
    url = url.split("/")
    data = '''[[["HoAMBc","[null,null,{},null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,{},null,null,null,null,null,null,null,null,{},null,false]",null,"generic"]]]'''.format(
        data1,
        request_ds1,
        data2,
    ).replace('None', 'null').replace(', ', ',').replace("\'", '\\"').replace('\n', '')
    data = {"f.req": data}
    next_url = "{}://{}/_/VisualFrontendUi/data/batchexecute?rpcids=HoAMBc&source-path=%2Fsearch&f.sid={}&bl={}&hl={}&authuser&soc-app=162&soc-platform=1&soc-device=1&_reqid={}&rt=c".format(
        url[0].split(":")[0],
        url[2],
        sid,
        bl,
        hl,
        _reqid,
    )
    # print(next_url)
    # print(data)
    if raw:
        return post_raw(next_url, data, k)
    else:
        return post(next_url, data, k)




#
#
#
#
# def search_videos(kw, page=1, raw=True):
#     return search(kw, cat="Videos", page=page, raw=raw)
#
#
# def search_news(kw, page=1, raw=True):
#     return search(kw, cat="News", page=page, raw=raw)


