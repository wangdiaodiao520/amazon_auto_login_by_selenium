# coding:utf-8
import requests
import urllib
import base64
import json


def img_yz_t(z,img,x,y):
    path = "img"+z+".jpg"
    rep = urllib.urlopen(img).read()
    with open(path, 'wb') as f:
        f.truncate()
        f.write(rep)
    #f = open(path, 'rb').read()
    with open(path, 'rb') as f:
        img_base64 = base64.b64encode(f.read())
        r = ShowapiRequest("http://route.showapi.com/184-5",x,y)
        r.addBodyPara("img_base64", img_base64)
        r.addBodyPara("typeId", "34")
        r.addBodyPara("convert_to_jpg", "0")
        r.addBodyPara("needMorePrecise", "0")
        # r.addFilePara("img", r"C:\Users\showa\Desktop\使用过的\4.png") #文件上传时设置
        res = r.post()
        return json.loads(res.text).get('showapi_res_body').get('Result')




files = {}
headers = {}
body = {}
timeouts = {}
resHeader = {}

class ShowapiRequest:
    def __init__(self, url, my_appId, my_appSecret):
        self.url = url
        self.my_appId = my_appId
        self.my_appSecret = my_appSecret
        body["showapi_appid"] = my_appId
        body["showapi_sign"] = my_appSecret
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2427.7 Safari/537.36"

    def addFilePara(self, key, value_url):
        files[key] = open(r"%s" % (value_url), 'rb')
        return self

    def addHeadPara(self, key, value):
        headers[key] = value
        return self

    def addBodyPara(self, key, value):
        body[key] = value
        return self
    #设置连接时间和读取时间
    def setTimeout(self, connecttimout, readtimeout):
        timeouts["connecttimout"] = connecttimout
        timeouts["readtimeout"] = readtimeout
        return self


    def get(self):
        get_url = self.url + "?" + urllib.urlencode(body)
        if not timeouts:
            res = requests.get(get_url, headers=headers)
        else:
            timeout = (timeouts["connecttimout"], timeouts["readtimeout"])
            res = requests.get(get_url, headers=headers, timeout=timeouts)
        return res

    def post(self):
        if not timeouts:
            res = requests.post(self.url, files=files, data=body, headers=headers)
        else:
            timeout = (timeouts["connecttimout"], timeouts["readtimeout"])
            res = requests.post(self.url, files=files, data=body, headers=headers, timeout=timeout)
        return res



if __name__ == "__main__":
    img = ''
    a = img_yz_t('5',img,90208,'8a753ab908424d7793da51d2790e7b72')
