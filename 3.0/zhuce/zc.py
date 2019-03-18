# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from phone import get_p,get_y
from error import *
from selenium import webdriver
from yz import img_yz,img_yz_t
from lxml import etree
from settings import *
import random
import time
import re
from proxy import ip


class Zc():
    def __init__(self,*zc_list):
        self.infor = zc_list

    def zc(self):
        try:
            #-------------------第一页------------------#
            #设置、声明浏览器
            dp = ''
            profile = webdriver.FirefoxOptions()
            if DISPLAY ==True:
                pass
            else:
                profile.add_argument('--headless')
            if P_CONTROL == False:
                pass
            else:
                profile.set_preference('browser.link.open_newwindow',3)
                profile.set_preference('network.proxy.type', 1)
                profile.set_preference('network.proxy.http', ip()[0])
                profile.set_preference('network.proxy.http_port', int(ip()[1]))
                profile.update_preferences()
            browser = webdriver.Firefox(firefox_options=profile)
            browser.set_page_load_timeout(TIMEOUT)
            #清除浏览器cookie，并请求amazon主页，生成新cookie
            browser.delete_all_cookies()
            time.sleep(3)
            #设置长等待600s，1秒一次检测，短等待10s，1秒一次检测
            wait_long = WebDriverWait(browser,LONG_TIMEOUT,1)
            wait_short = WebDriverWait(browser,SHORT_TIMEOUT)
            #打开amazon主页，出现输入框停止加载
            '''
            browser.get('https://amazon.com')
            wait_long.until(EC.presence_of_element_located((By.ID,'twotabsearchtextbox')))
            browser.execute_script("window.stop();")
            '''
            #打开注册页，检测加载情况，如出现指定元素则停止加载，防止js过长时间加载
            try:
                browser.get(URL)
            except TimeoutException:
                try:
                    wait_short.until(EC.presence_of_element_located((By.ID,'continue')))
                except:
                    browser.quit()
                    self.zc()
            if wait_long.until(EC.element_to_be_clickable((By.ID,'continue'))):
                browser.execute_script("window.stop();")
            #在新窗口打开临时邮箱
            js = 'window.open("https://bccto.me/");'
            browser.execute_script(js)
            #计算邮箱窗口权柄，转入邮箱窗口
            zc_handle = browser.current_window_handle
            handles = browser.window_handles
            mail_handle = None
            for handle in handles:
                if handle != zc_handle:
                    mail_handle = handle
            browser.switch_to.window(mail_handle)
            time.sleep(1)
            #等待页面加载出随机按钮，获取邮箱
            wait_long.until(EC.text_to_be_present_in_element((By.XPATH,'//span[@id="showmail"]'),'bccto.me'))
            html = etree.HTML(browser.page_source)
            email_adress_s = ''.join(html.xpath('//span[@id="showmail"]/text()')).strip()
            time.sleep(3)
            browser.find_element_by_id('randMail').click()
            time.sleep(3)
            browser.find_element_by_id('applyMail').click()
            time.sleep(3)
            html = etree.HTML(browser.page_source)
            email_adress_e = ''.join(html.xpath('//span[@id="showmail"]/text()')).strip()
            point_mail = email_adress_s == email_adress_e
            #判断是否申请到新邮箱，如否，重新申请
            global email_adress
            while point_mail:
                browser.find_element_by_id('randMail').click()
                time.sleep(3)
                browser.find_element_by_id('applyMail').click()
                time.sleep(3)
                html = etree.HTML(browser.page_source)
                email_adress_e = ''.join(html.xpath('//span[@id="showmail"]/text()')).strip()
                point_mail = email_adress_s == email_adress_e
            else:
                email_adress = email_adress_e
            #转入注册窗口，输入注册信息，并提交
            browser.switch_to.window(zc_handle)
            time.sleep(1)
            browser.find_element_by_id('ap_customer_name').send_keys(self.infor[0])
            time.sleep(1)
            browser.find_element_by_id('ap_email').send_keys(email_adress)
            time.sleep(1)
            browser.find_element_by_id('ap_password').send_keys(self.infor[1])
            time.sleep(1)
            browser.find_element_by_id('ap_password_check').send_keys(self.infor[1])
            time.sleep(1)
            #检测页面是否出现验证码，如出现，打码重新输入信息并提交
            try:
                browser.find_element_by_id('continue').click()
            except:
                if browser.find_element_by_id('auth-captcha-image') or browser.find_element_by_xpath('//*[@id="a-autoid-0"]/span/input'):
                    pass
                else:
                    browser.quit()
                    self.zc()
            title_point = 'Registration' in browser.title
            while title_point:
                wait_short.until(EC.presence_of_element_located((By.ID,'auth-captcha-image')))
                html = etree.HTML(browser.page_source)
                img = ''.join(html.xpath('//*[@id="auth-captcha-image"]/@src')).strip()
                try:#--------打码平台----------#
                    if YZ == 'img_yz':     
                        yzm = img_yz(img)
                    elif YZ == 'img_yz_t':                   
                        yzm = img_yz_t(img)
                    else:
                        raise YZ_none_error
                except:
                    raise YZ_error                
                print yzm
                browser.find_element_by_id('ap_password').send_keys(self.infor[1])
                time.sleep(1)
                browser.find_element_by_id('ap_password_check').send_keys(self.infor[1])
                time.sleep(1)
                for i in yzm:
                    browser.find_element_by_id('auth-captcha-guess').send_keys(i)
                    time.sleep(random.uniform(1,3))
                time.sleep(3)
                try:
                    browser.find_element_by_id('continue').click()
                except:
                    browser.quit()
                    self.zc()
                title_point = 'Registration' in browser.title
            else:
                pass
            #验证码无返回重新注册
            if 'Registration' in browser.title == True:
                browser.quit()
                self.zc()
            else:
                pass
            #检测是否出现可验证按钮，转入邮箱窗口
            if wait_long.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/form/div[4]/span/span/input'))):
                browser.execute_script("window.stop();")
            browser.switch_to.window(mail_handle)
            time.sleep(3)
            #检测，并等待页面刷新出邮件
            wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#inbox > tr:nth-child(2)')))
            #拼接邮件链接
            html = etree.HTML(browser.page_source)
            w = ''.join(html.xpath('/html/body/div[2]/div[3]/table/tbody/tr[2]/@fid'))
            z = email_adress.replace('@','(a)').replace('.','-_-')
            t = 'https://bccto.me/win/' + z + '/' + w
            js = 'window.open("{url}");'.format(url=t)
            #在新窗口打开邮件链接，获取邮件权柄，并转入邮件窗口
            browser.execute_script(js)
            handles = browser.window_handles
            yzm_handle = None
            for handle in handles:
                if handle != zc_handle and handle != mail_handle:
                    yzm_handle = handle
            browser.switch_to.window(yzm_handle)
            #检测并等待页面加载出邮件，获取邮箱验证码
            wait_long.until(EC.presence_of_element_located((By.ID,'content')))
            html = etree.HTML(browser.page_source)
            yxyzm = ''.join(html.xpath('//p[@class="otp"]/text()'))
            #转入注册页，输入邮箱验证码，点击提交
            browser.switch_to.window(zc_handle)
            wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.a-input-text'))).send_keys(yxyzm)
            time.sleep(1)
            browser.find_element_by_class_name('a-button-input').click()
            time.sleep(5)
            #-------------------第二页------------------#
            #检测并等待页面加载出输入框，进行输入，提交
            legal_name = wait_long.until(EC.presence_of_element_located((By.ID,'ln_legal_name')))
            time.sleep(3)
            legal_name.send_keys(self.infor[2])
            time.sleep(1)
            wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.a-icon-checkbox'))).click()
            time.sleep(3)
            wait_long.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[5]/div[5]/div[2]/div[2]/div[2]/div[2]/div/div/span/span/input')))               
            try:
                while browser.find_element_by_id('ln_legal_name'):
                    browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div[2]/div[2]/div[2]/div[2]/div/div/span/span/input').click()
                    time.sleep(60)                 
            except:
                pass

            #-------------------第三页------------------#
            #检测并等待页面加载出输入框
            wait_long.until(EC.presence_of_element_located((By.ID,'country-phone-input')))
            #地址选择中国
            wait_long.until(EC.presence_of_element_located((By.XPATH,'//*[@id="SuggestedAddress"]/div[2]/div[3]/div[1]/div/div[1]/select'))).click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="SuggestedAddress"]/div[2]/div[3]/div[1]/div/div[1]/select/option[@value="China"]').click()
            time.sleep(3)
            #输入地址信息
            browser.find_element_by_xpath('//*[@id="SuggestedAddress"]/div[2]/div[1]/div[1]/div/input').send_keys(self.infor[3])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="SuggestedAddress"]/div[2]/div[1]/div[2]/div/input').send_keys(self.infor[4])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="SuggestedAddress"]/div[2]/div[2]/div[1]/div/input').send_keys(self.infor[5])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="SuggestedAddress"]/div[2]/div[2]/div[2]/div/input').send_keys(self.infor[6])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="SuggestedAddress"]/div[2]/div[3]/div[2]/div/div[1]/input').send_keys(int(self.infor[7]))
            time.sleep(1)
            #商铺名称
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[3]/form/div/div[2]/div[1]/div/input').send_keys(self.infor[8])
            time.sleep(1)
            #选择中国号段
            browser.find_element_by_xpath('//*[@id="captchaid"]/div[2]/form/div[3]/div[1]/div/div[1]/div[1]/div/div/div').click()
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="captchaid"]/div[2]/form/div[3]/div[1]/div/div[1]/div[1]/div/div/ul/li[@data-dial-code="86"]').click()
            time.sleep(10)
            #---需加检测店铺名是否可用---#
            if wait_long.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[3]/form/div/div[2]/div[2]/div/div/div/div'))):
                html = etree.HTML(browser.page_source)
                aplybale = ''.join(html.xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[3]/form/div/div[2]/div[2]/div/div/div/div/text()'))
                if 'unavailable' in aplybale:
                    raise Business_name_error
                elif 'again' in aplybale:
                    browser.quit()
                    self.zc()
                else:
                    dp='店铺名可用'
                    print dp
                    pass
            #得到手机号，并输入
            global phone
            phone = get_p()
            for x in phone:
                browser.find_element_by_id('country-phone-input').send_keys(x)
                time.sleep(random.uniform(0.5,1.5))
            #检测手机号码是否出现异常？？？？？？？？？？？？？？？
            time.sleep(5)
            browser.find_element_by_id('country-phone-input').click()
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[5]/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div[2]/div/div[2]/span/span/button').click()
            time.sleep(3)
            #拿到验证码,并输入提交
            p_yzm = get_y(phone)
            point = 'success' not in p_yzm
            point_phone = 0
            while point and point_phone < 5:
                time.sleep(5)
                p_yzm = get_y(phone)
                point = 'success' not in p_yzm
                point_phone += 1
            else:
                if point == False:
                    p_yzm = re.sub("\D", "", p_yzm)
                else:
                    browser.quit()
                    self.zc()
            for i in p_yzm:
                browser.find_element_by_xpath('//*[@id="captchaid"]/div[2]/form/div[2]/div[2]/div/input').send_keys(i)
                time.sleep(random.uniform(0.5,1))
            browser.find_element_by_xpath('//*[@id="captchaid"]/div[2]/form/div[2]/div[2]/div/span/span/button').click()
            time.sleep(5)
            #判断是否跳页按钮可点击，如是则点击，判断是否跳页，如否，再次点击next
            title_s = browser.title
            wait_long.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[7]/div[2]/div/div/span/span/input'))).click()
            time.sleep(30)
            t_p = title_s == browser.title
            while t_p:
                wait_long.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[7]/div[2]/div/div/span/span/input'))).click()
                time.sleep(30)
                t_p = title_s == browser.title
            else:
                pass
            #-------------------第四页------------------#
            #提交信用卡等信息
            wait_long.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[8]/div[2]/div/div/div/span/span/input')))
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[1]/input').send_keys(int(self.infor[9]))
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[2]/div[2]/div[1]/div/select').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[2]/div[2]/div[1]/div/select/option[@value="{mouth}"]'.format(mouth=str(int(self.infor[10])-1))).click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[2]/div[2]/div[3]/div/select').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[2]/div[2]/div[3]/div/select/option[@value="{year}"]'.format(year=str(int(self.infor[11])-2019))).click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[3]/div/div[2]/div/input').send_keys(self.infor[12])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/input').send_keys(self.infor[12])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div/input').send_keys(self.infor[13])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/input').send_keys(int(self.infor[9]))
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/input').send_keys(int(self.infor[9]))
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[8]/div[2]/div/div/div/span/span/input').click()
            time.sleep(30)
            #判断是否跳页，如否，检查汇款路径是否可用，如可用填写信用卡号，重新next
            point_four = 'Deposit' in browser.title
            while point_four == True:
                html = etree.HTML(browser.page_source)
                if 'invalid' in ''.join(html.xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[3]/div/div/div/div/text()')):
                    raise Card_code_error
                else:
                    wait_long.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[8]/div[2]/div/div/div/span/span/input')))
                    browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div/div[2]/div/form[2]/div/div[1]/input').send_keys(self.infor[9])
                    time.sleep(1)
                    browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/div[2]/div[8]/div[2]/div/div/div/span/span/input').click()
                    time.sleep(30)
                    point_four = 'Deposit' in browser.title
            else:
                pass
            if 'Deposit' in browser.title ==True:
                browser.quit()
                self.zc()
            #-------------------第五页------------------#
            wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR,'input.ng-scope'))).click()
            time.sleep(15)
            #-------------------第六页------------------#
            wait_long.until(EC.presence_of_element_located((By.ID,'toggleButtonId_IsUSPerson_false')))
            browser.find_element_by_xpath('//*[@id="toggleButtonId_IsUSPerson_false"]/span/input').click()
            time.sleep(3)
            wait_long.until(EC.presence_of_element_located((By.ID,'a-autoid-13-announce'))).click()
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="a-popover-7"]/div/div/ul/li[@aria-labelledby="CountryOfCitizenshipCode_46"]/a').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_IndividualPersonName"]/input').send_keys(self.infor[12])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="selectionListDiv_NonUSPermCountryCode"]/span/span/span/span/span').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="a-popover-8"]/div/div/ul/li[@aria-labelledby="NonUSPermCountryCode_46"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_NonUSPermAddress1"]/input').send_keys(self.infor[3])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_NonUSPermAddress2"]/input').send_keys(self.infor[4])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_NonUSPermCity"]/input').send_keys(self.infor[5])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_NonUSPermStateTextbox"]/input').send_keys(self.infor[6])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_NonUSPermPC"]/input').send_keys(int(self.infor[7]))
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="editableContent_NonUSPermanentAddressEditableContentQuestion_button_done"]').click()
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="button_NonUSTaxIdentityInformationSectionSaveButton"]/span/span/span/button').click()
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="textBoxSingleDiv_ElectronicSignatureW8BenName"]/input').send_keys(self.infor[12])
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="button_SaveAndPreviewButtonW8Ben"]/span/span/span/button').click()
            time.sleep(15)
            #-------------------第七页------------------#
            wait_long.until(EC.presence_of_element_located((By.ID,'CustomHTMLFormsQuestion-question')))
            time.sleep(random.uniform(5,10))
            browser.find_element_by_xpath('//*[@id="button_SubmitButton"]/span/span/span/button').click()
            time.sleep(15)
            #-------------------第七页------------------#
            #点击退出提交信息按钮
            wait_long.until(EC.presence_of_element_located((By.ID,'exit-button-id'))).click()
            time.sleep(15)
            #-------------------第八页------------------#
            #如出现暂时跳过，则点击
            wait_long.until(EC.presence_of_element_located((By.ID,'productInterviewMain')))
            try:
                while wait_short.until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="productInterviewMain"]/div[1]/div[2]/a'),'Skip')):
                    browser.find_element_by_xpath('//*[@id="productInterviewMain"]/div[1]/div[2]/a').click()
                    time.sleep(10)
            except:
                pass
            try:
                while wait_short.until(EC.text_to_be_present_in_element((By.XPATH,'/html/body/div[1]/div/div[5]/div[6]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/a'),'Skip')):
                    browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[6]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/a').click()
                    time.sleep(10)
            except:
                pass
            #-------------------第九页------------------#
            wait_long.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[2]/div/div[7]/div[3]/div/div[2]/label/input'))).click()
            time.sleep(3)
            try:
                while wait_short.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[2]/div/div[7]/div[3]/div/div[2]/label/input'))):
                    browser.find_element_by_css_selector('.a-button-input').click()
                    time.sleep(10)
            except:
                pass
            #-------------------第十页------------------#
            wait_long.until(EC.presence_of_element_located((By.ID,'identityDocumentSelection')))
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[5]/div/div[2]/div[2]/input').send_keys(int(self.infor[14]))
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[5]/div/div[5]/div[2]/div[1]/span/select').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[5]/div/div[5]/div[2]/div[1]/span/select/option[@value="China"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[5]/div/div[5]/div[1]/div[1]/input').send_keys(self.infor[15])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[9]/div/div[1]/div/input').send_keys(self.infor[18])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[9]/div/div[2]/div/input').send_keys(self.infor[20])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[10]/div/div[1]/div/div[2]/input').send_keys(u'{}'.format(self.infor[17]))
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[10]/div/div[2]/div/div[2]/input').send_keys(u'{}'.format(self.infor[19]))
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[6]/div/div/form/div[1]/div[2]/div[11]/div/input').send_keys(self.infor[16])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[10]/div/div/form/div[2]/div[1]/div[1]/div/div/div[2]/div/input').send_keys(self.infor[8])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[10]/div/div/form/div[2]/div[1]/div[3]/div/input').send_keys(self.infor[21])
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[22]/div[2]/span/span/input').click()
            time.sleep(15)                 
            if wait_long.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[22]/div[2]/span/span/input'))):
                browser.execute_script("window.stop();")
            point_url = "sw/SSR/SIVInfo/step/DND" not in browser.current_url
            while point_url:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[22]/div[2]/span/span/input').click()
                time.sleep(15)
                wait_long.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[5]/div[3]/div/div[2]/div[22]/div[2]/span/span/inpu')))
                point_url = "sw/SSR/SIVInfo/step/DND" not in browser.current_url
            else:
                pass
        except Business_name_error:
            browser.quit()
            raise Business_name_error
        except Card_code_error:
            browser.quit()
            raise Card_code_error
        except YZ_error:
            browser.quit()
            raise YZ_error
        except:
            if '店铺' in dp:
                browser.quit()
                return email_adress
            else:
                browser.quit()
                self.zc()
        else:
            global result
            result = ['test','test']
            browser.quit()
            return result
        

def start(*zc_list):
    zc = Zc(*zc_list)
    result = zc.zc()
    return result


if __name__ == "__main__":
    zc_list = []
    start(*zc_list)
