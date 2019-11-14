from PIL import Image
import re
import  urllib.request

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

def go(fulls,no_jpg_name,right_jpg_name):
    locationlist = []
    fulljpg = ''
    for index,full in enumerate(fulls):
        fulllocation = {}
        cc = full.get_attribute('style')
        fullurl = re.findall(r'url\("(.*?)"\);',cc)[0].replace('webp','jpg')
        fulljpg = fullurl
        fulllocation['x'] = re.findall(r'background-position:(.*?)px .*?px;',cc)[0]
        fulllocation['y'] = re.findall(r'background-position:.*?px (.*?)px;',cc)[0]
        locationlist.append(fulllocation)
    urllib.request.urlretrieve(fulljpg,no_jpg_name)
    getfull(no_jpg_name,locationlist,right_jpg_name)

go(bgs,'luanba.jpg','bg.jpg')
go(fullbgs,'luanfullbg.jpg','fullbg.jpg')