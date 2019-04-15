# -*- coding: utf-8 -*-
import requests


def ip(url):
    rep = requests.get(url)
    return rep.text.replace('\r\n', '').split(':')


if __name__ == "__main__":
    p = ip()
    
