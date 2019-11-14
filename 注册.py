from selenium import webdriver
from selenium.webdriver import ActionChains
from PIL import Image
import re
import urllib.request
from time import sleep
import random


class jiyanpojie():
    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.distance = 0


    def getfull(self,namea,locationlist,right_jpg_name):
        old = Image.open(namea)
        new = Image.new('RGB',(260,116))  #260,116是完整验证码的大小，10x58的小方块一共有56块。一行26个，即260。上下两行，即116。
        shang = []
        xia = []
        # 切割
        for location in locationlist:
            if location['y'] == str(-58):
                shang.append(old.crop((abs(int(location['x'])),58,abs(int(location['x']))+10,116)))
            if location['y'] == str(0):
                xia.append(old.crop((abs(int(location['x'])),0,abs(int(location['x']))+10,58)))
        #粘贴
        i = 0
        for ima in shang:
            new.paste(ima,(i,0))   #根据图片左上角的坐标来粘贴
            i +=10
        i = 0
        for imx in xia:
            new.paste(imx,(i,58))
            i +=10
        new.save(right_jpg_name)


    def go(self,fulls,no_jpg_name,right_jpg_name):
        locationlist = []
        fullurl = ''
        for index,full in enumerate(fulls):
            fulllocation = {}
            cc = full.get_attribute('style')
            fullurl = re.findall(r'url\("(.*?)"\);',cc)[0].replace('webp','jpg')
            fulllocation['x'] = re.findall(r'background-position:(.*?)px .*?px;',cc)[0]
            fulllocation['y'] = re.findall(r'background-position:.*?px (.*?)px;',cc)[0]
            locationlist.append(fulllocation)
        print(fullurl)
        urllib.request.urlretrieve(fullurl,no_jpg_name)
        self.getfull(no_jpg_name,locationlist,right_jpg_name)

    def get_url(self):
        url = r'https://www.huxiu.com/'
        self.driver.get(url)
        sleep(2)
        self.driver.maximize_window()
        sleep(4)
        zhuce_button = self.driver.find_element_by_class_name('js-register')
        zhuce_button.click()
        sleep(4)

    def get_right_img(self):
        #获得带有缺口的图片源码
        bgs = self.driver.find_elements_by_class_name('gt_cut_bg_slice')
        #获得没有缺口的图片源码
        fullbgs = self.driver.find_elements_by_class_name('gt_cut_fullbg_slice')
        sleep(2)
        self.go(bgs, 'luanba.jpg', 'bg.jpg')
        self.go(fullbgs, 'luanfullbg.jpg', 'fullbg.jpg')



    # 判断颜色是否相近
    def is_similar_color(self,x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 100:
                return False
        return True

    # 计算距离
    def get_offset_distance(self,cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.jpg")
                    return x

    def get_distance(self):
        bg = Image.open('bg.jpg')
        fullbg = Image.open('fullbg.jpg')
        self.distance = self.get_offset_distance(bg,fullbg)
        print(self.distance)


    def move_huakuai(self):
        slideelements = self.driver.find_element_by_css_selector('.gt_slider_knob.gt_show')
        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        # 滑块是  45*50
        self.distance -= slideelements.size.get('width') / 2
        self.distance += 15
        print('偏移量：：',self.distance)
        # 滑块进行移动
        ActionChains(self.driver).click_and_hold(slideelements).perform()
        while self.distance>0:
            x = random.randint(10,25)
            if self.distance<10:
                x = random.randint(1,2)
            ActionChains(self.driver).move_by_offset(xoffset=x,yoffset=0).perform()
            self.distance -= x
            sleep(int(x/10)+0.5)
        ActionChains(self.driver).move_by_offset(xoffset=self.distance,yoffset=0).perform()
        ActionChains(self.driver).release(on_element=slideelements).perform()
        sleep(4)

    def result(self):
        info = self.driver.find_element_by_css_selector('.gt_info_text')
        content = info.get_attribute('textContent')
        return content
    def register(self):
        phone = input('请输入注册手机号：')
        self.driver.find_element_by_id('sms_username').send_keys(phone)
        sleep(2)
        self.driver.find_element_by_css_selector('.js-btn-captcha.btn-captcha').click()
        captcha = input('请输入短信验证码：')
        self.driver.find_element_by_id('sms_captcha').send_keys(captcha)
        self.driver.find_element_by_css_selector('.js-btn-sms-login.btn-login').click()

jiyan = jiyanpojie()
jiyan.get_url()
while True:
    jiyan.get_right_img()
    jiyan.get_distance()
    jiyan.move_huakuai()
    content = jiyan.result()
    print(content)
    if content[:4] == '再来一次':
        sleep(4)
        continue
    elif content[:4] == '验证通过':
        jiyan.register()
        break



