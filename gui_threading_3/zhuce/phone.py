# -*- coding: utf-8 -*-
import requests


class Phone_Yz():
    def __init__(self,token):
        self.token = token

    def get_phone(self):
        phone_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+self.token+'&itemid=1136&excludeno='
        rep = requests.get(phone_url)
        return rep.text.replace('success|', '')

    def get_yzm(self, phone):
        yzm_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token='+self.token+'&itemid=1136&mobile=' + phone + '&release=1'
        rep = requests.get(yzm_url)
        return rep.text


def get_p(token):
    p = Phone_Yz(token)
    phone = p.get_phone()
    return phone


def get_y(phone,token):
    p = Phone_Yz(token)
    yzm = p.get_yzm(phone)
    return yzm


if __name__ == "__main__":
    token = ''
    get_p(token)
    

