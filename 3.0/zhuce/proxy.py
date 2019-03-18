# -*- coding: utf-8 -*-
import requests
from settings import DL_URL

def ip():
    api_url = DL_URL
    rep = requests.get(api_url)
    return rep.text.replace('\r\n', '').split(':')


if __name__ == "__main__":
    p = ip()
    print p