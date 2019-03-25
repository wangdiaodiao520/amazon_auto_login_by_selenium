# coding:utf-8
#from ShowapiRequest.ShowapiRequest import ShowapiRequest
#from .settings import CJY_user,CJY_password,CJY_id
from hashlib import md5
import requests
import urllib
import base64
import json
import os
import time


def img_yz_t(z,img,x,y):
    path = "img"+z+".jpg"
    if os.path.exists(path):
        os.remove(path)
    else:
        pass
    rep = urllib.urlopen(img).read()
    f = open(path, 'wb')
    f.write(rep)
    f.close()
    f = open(path, 'rb').read()
    #with open(path, 'rb') as f:
    img_base64 = base64.b64encode(f)
    r = ShowapiRequest("http://route.showapi.com/184-5",x,y)
    r.addBodyPara("img_base64", img_base64)
    r.addBodyPara("typeId", "34")
    r.addBodyPara("convert_to_jpg", "0")
    r.addBodyPara("needMorePrecise", "0")
    # r.addFilePara("img", r"C:\Users\showa\Desktop\使用过的\4.png") #文件上传时设置
    res = r.post()
    return json.loads(res.text).get('showapi_res_body').get('Result')


def img_yz_m(img):
    try:
        path = "img.jpg"
        if os.path.exists(path):
            os.remove(path)
        else:
            pass
        rep = urllib.urlopen(img).read()
        f = open(path, 'wb')
        f.write(rep)
        f.close()

        cjy = Chaojiying_Client('w15075747143', 'wangyunlong81', 'de262a074e958ff91dc134a75b3c0b86')
        im = open(path, 'rb').read()
        txt = cjy.PostPic(im, 1006).get('pic_str')
    except:
        img_yz(img)
    return txt


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

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

def img_get(x):
    path = "img.jpg"
    if os.path.exists(path):
        os.remove(path)
    else:
        pass
    rep = urllib.urlopen(x).read()
    f = open(path, 'wb')
    f.write(rep)
    f.close()
    f = open(path, 'rb').read()
    #with open(path, 'rb') as f:
    #img_base64 = rep
    return base64.b64encode(f)


if __name__ == "__main__":
    img = 'https://opfcaptcha-prod.s3.amazonaws.com/b228d301437f48e59d1b636557d6465c.jpg?AWSAccessKeyId=AKIAIL3FL7FBSK6NZUZA&Expires=1553452371&Signature=u0TBbS8AZ%2Bn2RsH8cXky6BDyUSw%3D'
    a = img_yz(img,90208,'8a753ab908424d7793da51d2790e7b72')
    print a
