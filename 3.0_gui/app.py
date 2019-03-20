# -*- coding: utf-8 -*-
import threading
from Tkinter import *
from zhuce.zc import start
from zhuce.error import *
import xlrd


log_num = 0

class GUI():
    def __init__(self,init_window):
        self.init_window = init_window

    def set_window(self):
        self.init_window.title(u"amazon__auto_register  by:王钢蛋")
        self.init_window.geometry(u'500x300+400+200')

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

        #self.display_label = Label(self.init_window)
        #self.display_label.grid(row=10, column=0)
        #self.display_label = Label(self.init_window)
        #self.display_label.grid(row=11, column=0)

        self.start_button = Button(self.init_window, text=u"开始", bg="lightblue", width=10,command=lambda:self.thread_it(self.run))
        self.start_button.grid(row=12, column=0)

        self.log_label = Label(self.init_window,)
        self.log_label.grid(row=0, column=1)

        self.log_label = Label(self.init_window,text=u"状态")
        self.log_label.grid(row=0, column=2)
        self.log_text = Text(self.init_window,width=35, height=18)
        self.log_text.grid(row=1, column=2,rowspan=11,columnspan=1)


    def write_log(self,logmsg):
        global log_num
        logmsg = logmsg + "\n"
        if log_num <= 8:
            self.log_text.insert(END,logmsg)
            log_num += 1
        else:
            self.log_text.delete(1.0,2.0)
            self.log_text.insert(END,logmsg)

    def log(self,i, statues, mail, phone):
        f = open('log.txt','a+')
        f.writelines(str(i+1)+','+statues+','+mail+','+phone+'\n')
        f.close()
        

    def run(self):
        dl_api = self.dl_api_text.get(1.0,END)
        time = int(self.timeout_text.get(1.0,END))
        yy_id = self.yy_id_text.get(1.0,END)
        yy_sec = self.yy_sec_text.get(1.0,END)
        ym_token = self.ym_token_text.get(1.0,END)
        display = str(self.display_text.get(1.0,END))
        infor_sheet = xlrd.open_workbook('information.xlsx').sheet_by_index(0)
        infor_max = infor_sheet.nrows
        self.write_log(u"***共"+str(infor_max)+u"条信息需要注册***")
        if 'true' in display:
            self.write_log(u"———无界面模式")
        else:
            self.write_log(u"———有界面模式")
        if len(dl_api) >= 10:
            self.write_log(u"———使用代理")
        else:
            self.write_log(u"———未使用代理")
        for i in range(infor_max):
            self.write_log(u"开始注册第"+str(i+1)+u"条信息")
            zc_list = infor_sheet.row_values(i)
            try:
                result = start(dl_api,time,yy_id,yy_sec,ym_token,display,*zc_list)
                if type(result).__name__ == 'list':
                    self.write_log(u'第' + str(i + 1) + u'条信息注册成功，开始注册下一条')
                    self.log(i, 'success', result[0], result[1])
                else:
                    self.write_log(u'网络阻塞，且商户名已注册，记录此条信息，开始注册下一条')
                    self.log(i,'inter_error and bis_name_apply',result,'none')
            except Business_name_error:
                self.write_log(u'第'+str(i + 1) + u'条信息商户名无法注册，开始注册下一条')
                self.log(i, 'bis_name_error', 'none', 'none')
            except Card_code_error:
                self.write_log(u'第'+str(i + 1) + u'条信息9位汇款路径码无法注册，开始注册下一条')
                self.log(i, '9_code_error', 'none', 'none')
            except YZ_error:
                self.write_log(u'第三方验证出错，程序中止，请检查')
                break
        self.write_log(u'所有信息注册流程完成')
                
    @staticmethod
    def thread_it(func):
        t = threading.Thread(target=func) 
        t.setDaemon(True)   
        t.start()       
        # t.join()   
                                   
        
        

def gui_start():
    init_window = Tk()
    window = GUI(init_window)
    window.set_window()
    init_window.mainloop() 
    
gui_start()
