# -*- coding: utf-8 -*-
from settings import YM_id,YM_password
import requests


class Phone_Yz():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_token(self):
        token_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username=' + self.username + '&password=' + self.password
        rep = requests.get(token_url)
        return rep.text.replace('success|', '')

    def get_phone(self):
        phone_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + self.get_token() + '&itemid=1136&excludeno='
        rep = requests.get(phone_url)
        return rep.text.replace('success|', '')

    def get_yzm(self, phone):
        yzm_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=' + self.get_token() + '&itemid=1136&mobile=' + phone + '&release=1'
        rep = requests.get(yzm_url)
        return rep.text


def get_p():
    p = Phone_Yz(YM_id, YM_password)
    phone = p.get_phone()
    return phone


def get_y(phone):
    p = Phone_Yz(YM_id, YM_password)
    yzm = p.get_yzm(phone)
    return yzm


if __name__ == "__main__":
    p = get_p()
    # y = get_y('15031584213')
    print p