# -*- coding: utf-8 -*-
import threading
from Tkinter import *
from zhuce.zc import *
from zhuce.error import *
import xlrd
import time



log_num_1 = 0
log_num_2 = 0
log_num_3 = 0


class GUI():
    def __init__(self,init_window):
        self.init_window = init_window

    def set_window(self):
        self.init_window.title(u"amazon__auto_register  by:王钢蛋")
        self.init_window.geometry(u'1000x300+200+200')

        self.dl_api_label = Label(self.init_window,text=u"代理api")
        self.dl_api_label.grid(row=0, column=0)
        self.dl_api_text = Text(self.init_window,width=30, height=1)
        self.dl_api_text.grid(row=1, column=0)

        self.timeout_label = Label(self.init_window,text=u"超时设置")
        self.timeout_label.grid(row=2, column=0)
        self.timeout_text = Text(self.init_window,width=30, height=1)
        self.timeout_text.grid(row=3, column=0)

        self.yy_id_label = Label(self.init_window,text=u"易源id")
        self.yy_id_label.grid(row=4, column=0)
        self.yy_id_text = Text(self.init_window,width=30, height=1)
        self.yy_id_text.grid(row=5, column=0)

        self.yy_sec_label = Label(self.init_window,text=u"易源secret")
        self.yy_sec_label.grid(row=6, column=0)
        self.yy_sec_text = Text(self.init_window,width=30, height=1)
        self.yy_sec_text.grid(row=7, column=0)

        self.ym_token_label = Label(self.init_window,text=u"易码token")
        self.ym_token_label.grid(row=8, column=0)
        self.ym_token_text = Text(self.init_window,width=30, height=1)
        self.ym_token_text.grid(row=9, column=0)

        self.display_label = Label(self.init_window,text=u"有无界面")
        self.display_label.grid(row=10, column=0)
        self.display_text = Text(self.init_window,width=30, height=1)
        self.display_text.grid(row=11, column=0)


        self.log_label = Label(self.init_window,)
        self.log_label.grid(row=0, column=1)
        self.start_button_1 = Button(self.init_window, text=u"开始—1", bg="lightblue", width=10,command=lambda:self.thread_it(self.run_1))
        self.start_button_1.grid(row=0, column=2)
        self.log_text_1 = Text(self.init_window,width=35, height=18)
        self.log_text_1.grid(row=1, column=2,rowspan=11,columnspan=1)

        self.log_label = Label(self.init_window,)
        self.log_label.grid(row=0, column=3)
        self.start_button_2 = Button(self.init_window, text=u"开始—2", bg="lightblue", width=10,command=lambda:self.thread_it(self.run_2))
        self.start_button_2.grid(row=0, column=4)
        self.log_text_2 = Text(self.init_window,width=35, height=18)
        self.log_text_2.grid(row=1, column=4,rowspan=11,columnspan=1)

        self.log_label = Label(self.init_window,)
        self.log_label.grid(row=0, column=5)
        self.start_button_3 = Button(self.init_window, text=u"开始—3", bg="lightblue", width=10,command=lambda:self.thread_it(self.run_3))
        self.start_button_3.grid(row=0, column=6)
        self.log_text_3 = Text(self.init_window,width=35, height=18)
        self.log_text_3.grid(row=1, column=6,rowspan=11,columnspan=1)

        


    def write_log_1(self,logmsg):
        global log_num_1
        logmsg = logmsg + "\n"
        if log_num_1 <= 15:
            self.log_text_1.insert(END,logmsg)
            log_num_1 += 1
        else:
            self.log_text_1.delete(8.0,9.0)
            self.log_text_1.insert(END,logmsg)

    def write_log_2(self,logmsg):
        global log_num_2
        logmsg = logmsg + "\n"
        if log_num_2 <= 15:
            self.log_text_2.insert(END,logmsg)
            log_num_2 += 1
        else:
            self.log_text_2.delete(8.0,9.0)
            self.log_text_2.insert(END,logmsg)

    def write_log_3(self,logmsg):
        global log_num_3
        logmsg = logmsg + "\n"
        if log_num_3 <= 15:
            self.log_text_3.insert(END,logmsg)
            log_num_3 += 1
        else:
            self.log_text_3.delete(8.0,9.0)
            self.log_text_3.insert(END,logmsg)


    def run_1(self):
        MAIL = 'bccto.me'
        point = '1'
        dl_api = self.dl_api_text.get('0.0',END).strip()
        while dl_api == "None":
            dl_api = self.dl_api_text.get('0.0',END).strip()
        else:
            dl_api = dl_api.strip()
        timeout = self.timeout_text.get('0.0',END).strip()
        while timeout.isdigit() == False:
            timeout = self.timeout_text.get('0.0',END).strip()
        else:
            timeout = int(timeout)
            #time = int(self.timeout_text.get('0.0',END).strip())
        yy_id = self.yy_id_text.get('0.0',END).strip()
        while yy_id.isdigit() == False:
            yy_id = self.yy_id_text.get('0.0',END).strip()
        else:
            yy_id = int(yy_id)
            #yy_id = int(self.yy_id_text.get('0.0',END).strip())
        yy_sec = self.yy_sec_text.get('0.0',END).strip()
        while yy_sec == "None":
            yy_sec = self.yy_sec_text.get('0.0',END).strip()
        else:
            yy_sec = yy_sec.strip()
        ym_token = self.ym_token_text.get('0.0',END).strip()
        while ym_token == "None":
            ym_token = self.ym_token_text.get('0.0',END).strip()
        else:
            ym_token = ym_token.strip()
        display = self.display_text.get('0.0',END).strip()
        while display == "None":
            display = self.display_text.get('0.0',END).strip()
        else:
            display = display.strip()
        infor_sheet = xlrd.open_workbook('information_1.xlsx').sheet_by_index(0)
        infor_max = infor_sheet.nrows
        self.write_log_1(u"***共"+str(infor_max)+u"条信息需要注册***")
        if 'true' in display:
            self.write_log_1(u"———无界面模式")
        else:
            self.write_log_1(u"———有界面模式")
        if len(dl_api) >= 10:
            self.write_log_1(u"———使用代理")
        else:
            self.write_log_1(u"———未使用代理")
        self.write_log_1(u"超时设置为："+str(timeout)+"s")
        self.write_log_1(u"易源id为："+str(yy_id))
        self.write_log_1(u"易源secret为："+yy_sec)
        self.write_log_1(u"易码token为："+ym_token)
        for i in range(infor_max):
            self.write_log_1(u"开始注册第"+str(i+1)+u"条信息")
            zc_list = infor_sheet.row_values(i)
            try:
                zc_1 = Zc(dl_api,timeout,yy_id,yy_sec,ym_token,display,point,MAIL,i,*zc_list)
                zc_1.zc()
            except Business_name_error:
                self.write_log_1(u'第'+str(i + 1) + u'条信息商户名无法注册，开始注册下一条')
            except Card_code_error:
                self.write_log_1(u'第'+str(i + 1) + u'条信息9位汇款路径码无法注册，开始注册下一条')
            except TIMEOUT_error:
                self.write_log_1(u'网络阻塞，且商户名已注册，记录此条信息，开始注册下一条')
            else:
                self.write_log_1(u'第' + str(i + 1) + u'条信息注册成功，开始注册下一条')
        self.write_log_1(u'所有信息注册流程完成')

    def run_2(self):
        MAIL = 'bccto.me'
        point = '2'
        dl_api = self.dl_api_text.get('0.0',END).strip()
        while dl_api == "None":
            dl_api = self.dl_api_text.get('0.0',END).strip()
        else:
            dl_api = dl_api.strip()
        timeout = self.timeout_text.get('0.0',END).strip()
        while timeout.isdigit() == False:
            timeout = self.timeout_text.get('0.0',END).strip()
        else:
            timeout = int(timeout)
            #time = int(self.timeout_text.get('0.0',END).strip())
        yy_id = self.yy_id_text.get('0.0',END).strip()
        while yy_id.isdigit() == False:
            yy_id = self.yy_id_text.get('0.0',END).strip()
        else:
            yy_id = int(yy_id)
            #yy_id = int(self.yy_id_text.get('0.0',END).strip())
        yy_sec = self.yy_sec_text.get('0.0',END).strip()
        while yy_sec == "None":
            yy_sec = self.yy_sec_text.get('0.0',END).strip()
        else:
            yy_sec = yy_sec.strip()
        ym_token = self.ym_token_text.get('0.0',END).strip()
        while ym_token == "None":
            ym_token = self.ym_token_text.get('0.0',END).strip()
        else:
            ym_token = ym_token.strip()
        display = self.display_text.get('0.0',END).strip()
        while display == "None":
            display = self.display_text.get('0.0',END).strip()
        else:
            display = display.strip()
        infor_sheet = xlrd.open_workbook('information_2.xlsx').sheet_by_index(0)
        infor_max = infor_sheet.nrows
        self.write_log_2(u"***共"+str(infor_max)+u"条信息需要注册***")
        if 'true' in display:
            self.write_log_2(u"———无界面模式")
        else:
            self.write_log_2(u"———有界面模式")
        if len(dl_api) >= 10:
            self.write_log_2(u"———使用代理")
        else:
            self.write_log_2(u"———未使用代理")
        self.write_log_2(u"超时设置为："+str(timeout)+"s")
        self.write_log_2(u"易源id为："+str(yy_id))
        self.write_log_2(u"易源secret为："+yy_sec)
        self.write_log_2(u"易码token为："+ym_token)
        time.sleep(60)
        for i in range(infor_max):
            self.write_log_2(u"开始注册第"+str(i+1)+u"条信息")
            zc_list = infor_sheet.row_values(i)
            try:
                zc_2 = Zc(dl_api,timeout,yy_id,yy_sec,ym_token,display,point,MAIL,i,*zc_list)
                zc_2.zc()
            except Business_name_error:
                self.write_log_2(u'第'+str(i + 1) + u'条信息商户名无法注册，开始注册下一条')
            except Card_code_error:
                self.write_log_2(u'第'+str(i + 1) + u'条信息9位汇款路径码无法注册，开始注册下一条')
            except TIMEOUT_error:
                self.write_log_2(u'网络阻塞，且商户名已注册，记录此条信息，开始注册下一条')
            else:
                self.write_log_2(u'第' + str(i + 1) + u'条信息注册成功，开始注册下一条')
        self.write_log_2(u'所有信息注册流程完成')

    def run_3(self):
        MAIL = 'bccto.me'
        point = '3'
        dl_api = self.dl_api_text.get('0.0',END).strip()
        while dl_api == "None":
            dl_api = self.dl_api_text.get('0.0',END).strip()
        else:
            dl_api = dl_api.strip()
        timeout = self.timeout_text.get('0.0',END).strip()
        while timeout.isdigit() == False:
            timeout = self.timeout_text.get('0.0',END).strip()
        else:
            timeout = int(timeout)
            #time = int(self.timeout_text.get('0.0',END).strip())
        yy_id = self.yy_id_text.get('0.0',END).strip()
        while yy_id.isdigit() == False:
            yy_id = self.yy_id_text.get('0.0',END).strip()
        else:
            yy_id = int(yy_id)
            #yy_id = int(self.yy_id_text.get('0.0',END).strip())
        yy_sec = self.yy_sec_text.get('0.0',END).strip()
        while yy_sec == "None":
            yy_sec = self.yy_sec_text.get('0.0',END).strip()
        else:
            yy_sec = yy_sec.strip()
        ym_token = self.ym_token_text.get('0.0',END).strip()
        while ym_token == "None":
            ym_token = self.ym_token_text.get('0.0',END).strip()
        else:
            ym_token = ym_token.strip()
        display = self.display_text.get('0.0',END).strip()
        while display == "None":
            display = self.display_text.get('0.0',END).strip()
        else:
            display = display.strip()
        infor_sheet = xlrd.open_workbook('information_3.xlsx').sheet_by_index(0)
        infor_max = infor_sheet.nrows
        self.write_log_3(u"***共"+str(infor_max)+u"条信息需要注册***")
        if 'true' in display:
            self.write_log_3(u"———无界面模式")
        else:
            self.write_log_3(u"———有界面模式")
        if len(dl_api) >= 10:
            self.write_log_3(u"———使用代理")
        else:
            self.write_log_3(u"———未使用代理")
        self.write_log_3(u"超时设置为："+str(timeout)+"s")
        self.write_log_3(u"易源id为："+str(yy_id))
        self.write_log_3(u"易源secret为："+yy_sec)
        self.write_log_3(u"易码token为："+ym_token)
        time.sleep(120)
        for i in range(infor_max):
            self.write_log_3(u"开始注册第"+str(i+1)+u"条信息")
            zc_list = infor_sheet.row_values(i)
            try:
                zc_3 = Zc(dl_api,timeout,yy_id,yy_sec,ym_token,display,point,MAIL,i,*zc_list)
                zc_3.zc()
            except Business_name_error:
                self.write_log_3(u'第'+str(i + 1) + u'条信息商户名无法注册，开始注册下一条')
            except Card_code_error:
                self.write_log_3(u'第'+str(i + 1) + u'条信息9位汇款路径码无法注册，开始注册下一条')
            except TIMEOUT_error:
                self.write_log_3(u'网络阻塞，且商户名已注册，记录此条信息，开始注册下一条')
            else:
                self.write_log_3(u'第' + str(i + 1) + u'条信息注册成功，开始注册下一条')          
        self.write_log_3(u'所有信息注册流程完成')

                
    @staticmethod
    def thread_it(func):
        t = threading.Thread(target=func) 
        t.setDaemon(True)   
        t.start()       
        #t.join()   
                                   
        
        

def gui_start():
    init_window = Tk()
    window = GUI(init_window)
    window.set_window()
    init_window.mainloop() 
    
gui_start()
