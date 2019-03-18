# coding:utf-8
from ShowapiRequest.ShowapiRequest import ShowapiRequest
from settings import CJY_user,CJY_password,CJY_id,YY_id,YY_secret
from hashlib import md5
import requests
import urllib
import base64
import json
import os


def img_yz_t(img):
    path = "img.jpg"
    if os.path.exists(path):
        os.remove(path)
    else:
        pass
    rep = urllib.urlopen(img).read()
    f = open(path, 'wb')
    f.write(rep)
    f.close()
    f = open(path, 'rb').read()
    with open(path, 'rb') as f:
        img_base64 = base64.b64encode(f.read())
        r = ShowapiRequest("http://route.showapi.com/184-5", YY_id,YY_secret)
        r.addBodyPara("img_base64", img_base64)
        r.addBodyPara("typeId", "34")
        r.addBodyPara("convert_to_jpg", "0")
        r.addBodyPara("needMorePrecise", "0")
        # r.addFilePara("img", r"C:\Users\showa\Desktop\使用过的\4.png") #文件上传时设置
        res = r.post()
        return json.loads(res.text).get('showapi_res_body').get('Result')


def img_yz(img):
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

        cjy = Chaojiying_Client(CJY_user, CJY_password, CJY_id)
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


if __name__ == "__main__":
    img = ""
    img_yz_t(img)
