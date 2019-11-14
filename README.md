# selenium_slider
selenium模拟虎嗅极验滑块


selenium破解滑块应该是老生常谈的话题，今天我就总结一下破解虎嗅极速注册滑块的步骤。
导入功能库

    from selenium import webdriver
    from selenium.webdriver import ActionChains
    from PIL import Image
    import re
    import urllib.request
    from time import sleep
    import random

#### 1.进入注册页面

    driver = webdriver.Chrome('chromedriver.exe')
    url = r'https://www.huxiu.com/'
    driver.get(url)
    #浏览器最大化 确保计算距离的准确性
    driver.maximize_window()
    sleep(6)
    #点击注册
    zhuce_button = driver.find_element_by_class_name('js-register')
    zhuce_button.click()
    sleep(3)
#### 2.获取正常的滑块图片

    #获得带有缺口的图片标签
    bgs = driver.find_elements_by_class_name('gt_cut_bg_slice')
    #获得没有缺口的图片标签
    fullbgs = driver.find_elements_by_class_name('gt_cut_fullbg_slice')
    sleep(3)

    #根据坐标拼接正确的图片
    def getfull(namea,locationlist,right_jpg_name):
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

    #获取每一小块图片的坐标
    def go(fulls,no_jpg_name,right_jpg_name):
        locationlist = []
        fullurl = ''
        for index,full in enumerate(fulls):
            fulllocation = {}
            cc = full.get_attribute('style')
            fullurl = re.findall(r'url\("(.*?)"\);',cc)[0].replace('webp','jpg')
            fulllocation['x'] = re.findall(r'background-position:(.*?)px .*?px;',cc)[0]
            fulllocation['y'] = re.findall(r'background-position:.*?px (.*?)px;',cc)[0]
        locationlist.append(fulllocation)
        urllib.request.urlretrieve(fullurl,no_jpg_name)
        getfull(no_jpg_name,locationlist,right_jpg_name)
    
    #因为获得的图片被打乱了，所以需要重组图片
    go(bgs,'luanba.jpg','bg.jpg')
    go(fullbgs,'luanfullbg.jpg','fullbg.jpg')

####3.缺口位置的计算

   #####第一种方法

    def offset(yes,no,x,y):
        # 获得图片上每个坐标点的RGB像素
        pix1 = yes.getpixel((x,y))
        pix2 = no.getpixel((x,y))
        for rgb in range(0,3):
            # 50 55 60 100
            if abs(pix1[rgb] - pix2[rgb]) > 100:
                return x  #这就是偏移量

    def compare(yes,no):
        for xzhou in range(0,260):
            for yzhou in range(0,116):
                pianyi = offset(yes,no,xzhou,yzhou)
                if pianyi == None:
                    pass
                else:
                    return pianyi


    yes = Image.open('bg.jpg')
    no = Image.open('fullbg.jpg')
    pianyishu = compare(yes,no)
    print('偏移量：','*'*20)
    print(pianyishu)
    print('*'*20)

#####第二种方法
    # 判断颜色是否相近
    def is_similar_color(x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 100:
                return False
        return True

    # 计算距离
    def get_offset_distance(cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.jpg")
                    return x

    bg = Image.open('bg.jpg')
    fullbg = Image.open('fullbg.jpg')
    distance = get_offset_distance(bg,fullbg)
    print('偏移量：：',distance)
####4.滑块移动
    
    #锁定滑块标签
    slideelements = driver.find_element_by_css_selector('.gt_slider_knob.gt_show')

    # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
    # 滑块是  45*50
    distance -= slideelements.size.get('width') / 2
    distance += 15
    print(distance)

    # 滑块进行移动
    ActionChains(driver).click_and_hold(slideelements).perform()
    while distance>0:
        #滑块距离缺口为10时改变滑动速度
        x = random.randint(10,25)
        if distance<10:
            x = random.randint(1,2)
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
        distance -= x
        sleep(int(x/10)+0.5)
    ActionChains(driver).move_by_offset(xoffset=distance,yoffset=0).perform()
    ActionChains(driver).release(on_element=slideelements).perform()
    sleep(4)
    
    #判断滑块是否移动成功
    info = driver.find_element_by_css_selector('.gt_info_text')
    #因为info标签是隐藏状态，所以不能用text()方法获取标签内容
    content = info.get_attribute('textContent')
    print(content)
    if content[:4] == '验证通过':
        phone = input('请输入注册手机号：')
        self.driver.find_element_by_id('sms_username').send_keys(phone)
        sleep(2)
        self.driver.find_element_by_css_selector('.js-btn-captcha.btn-captcha').click()
        captcha = input('请输入短信验证码：')
        self.driver.find_element_by_id('sms_captcha').send_keys(captcha)
        self.driver.find_element_by_css_selector('.js-btn-sms-login.btn-login').click()







