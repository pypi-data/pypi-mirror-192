from .utils import search_by_image, json_decode
import time
import re


def search(url, page=1, **kwargs):
    return search_by_image(url, page=page, **kwargs)


def get(**kwargs):
    from .images import process, parse
    for i in range(0, 5):
        try:
            r = search(**kwargs)
            if not re.search(rb"(\[\[.*?\]\])\n", r):
                raise
            return process(parse(r))
        except Exception as e:
            if i == 4:
                raise e
            time.sleep(5)

