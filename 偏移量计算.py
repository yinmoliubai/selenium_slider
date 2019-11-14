from PIL import Image



第一种方法
def is_pixel_equal(image, x, y, left_list):
    """
    判断两个像素是否相同
    :param image: 图片
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pixel1 = image.load()[x, y]
    threshold = 150
    # count记录一次向右有多少个像素点R、G、B都是小于150的
    count = 0
    # 如果该点的R、G、B都小于150，就开始向右遍历，记录向右有多少个像素点R、G、B都是小于150的
    if pixel1[0] < threshold and pixel1[1] < threshold and pixel1[2] < threshold:
        for i in range(x + 1, image.size[0]):
            piexl = image.load()[i, y]
            if piexl[0] < threshold and piexl[1] < threshold and piexl[2] < threshold:
                count += 1
            else:
                break
    if int(image.size[0]/8.6) < count < int(image.size[0]/4.3):
        left_list.append((x, count))
        return True
    else:
        return False


def get_gap(image):
    """
    获取缺口偏移量
    :param image: 带缺口图片
    :return:
    """
    # left_list保存所有符合条件的x轴坐标
    left_list = []
    # 我们需要获取的是凹槽的x轴坐标，就不需要遍历所有y轴，遍历几个等分点就行
    for i in [10*i for i in range(1,int(image.size[1]/11))]:
        # x轴从x为image.size[0]/5.16的像素点开始遍历，因为凹槽不会在x轴为50以内
        for j in range(int(image.size[0]/5.16),image.size[0]-int(image.size[0]/8.6)):
            if is_pixel_equal(image,j,i,left_list):
                break
    return left_list


if __name__ == '__main__':
    image = Image.open("bg.jpg")
    image = image.convert("RGB")
    left_list = get_gap(image)
    print(left_list)



第二种方法
判断颜色是否相近
def is_similar_color(x_pixel, y_pixel):
    for i, pixel in enumerate(x_pixel):
        if abs(y_pixel[i] - pixel) > 55:
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
a = get_offset_distance(bg,fullbg)

print(a)


第三种方法
def offset(yes,no,x,y):
    # 获得图片上每个坐标点的RGB像素
    pix1 = yes.getpixel((x,y))
    pix2 = no.getpixel((x,y))
    for rgb in range(0,3):
        # 50 55 60 100
        if abs(pix1[rgb] - pix2[rgb]) > 100:
            # print (x)
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







