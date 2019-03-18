# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException
from zhuce.zc import start
from zhuce.error import *
import time
import xlrd


infor_sheet = xlrd.open_workbook('information.xlsx').sheet_by_index(0)
infor_max = infor_sheet.nrows


def log(i, statues, mail, phone):
    f = open('log.txt','a+')
    f.writelines(str(i+1)+','+statues+','+mail+','+phone+'\n')
    f.close()

def run(i):
    print '开始注册第' + str(i + 1) + '条信息'
    zc_list = infor_sheet.row_values(i)
    try:
        result = start(*zc_list)
        print result
        if type(result).__name__ == 'list':
            print '第' + str(i + 1) + '条信息注册成功，开始注册下一条'
            log(i, 'success', result[0], result[1])
        else:
            print '网络阻塞，且商户名已注册，记录此条信息，开始注册下一条'
            log(i, 'inter_error and bis_name_apply', result, 'none')
    except Business_name_error:
        print '第'+str(i + 1) + '条信息商户名无法注册，开始注册下一条'
        log(i, 'bis_name_error', 'none', 'none')
    except Card_code_error:
        print '第'+str(i + 1) + '条信息9位汇款路径码无法注册，开始注册下一条'
        log(i, '9_code_error', 'none', 'none')
    except YZ_error:
        raise YZ_error


for i in range(infor_max):
    try:
        run(i)
    except YZ_error:
        print '第三方验证出现错误'
    #zc_list = infor_sheet.row_values(i)
    #start(*zc_list)
print '注册完成'
