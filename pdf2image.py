import os
import fitz
import re
import pytesseract
from PIL import Image

def pdf2image(path_pdf,path_pic):
    # 使用正则表达式来查找图片
    checkXO = r"/Type(?= */XObject)"
    checkIM = r"/Subtype(?= */Image)"
    # 打开pdf
    doc = fitz.open(path_pdf)
    # 图片计数
    imgcount = 0
    lenXREF = doc._getXrefLength()
    # 打印PDF的信息
    newnamepathList = []
    print("文件名:{}, 页数: {}, 对象: {}".format(path_pdf, len(doc), lenXREF - 1))
    # 遍历每一个对象

    for i in range(1, lenXREF):
        # 定义对象字符串
        text = doc._getXrefString(i)
        isXObject = re.search(checkXO, text)
        # 使用正则表达式查看是否是图片
        isImage = re.search(checkIM, text)
        # 如果不是对象也不是图片，则continue
        if not isXObject or not isImage:
            continue
        imgcount += 1
        # 根据索引生成图像
        pix = fitz.Pixmap(doc, i)
        # 根据pdf的路径生成图片的名称
        new_name1 = os.path.basename(path_pdf)
        new_name = new_name1[0:new_name1.find('.')] + "{}.png".format(imgcount)
        print(new_name)
        # 如果pix.n<5,可以直接存为PNG
        if pix.n < 5:
            pix.writePNG(os.path.join(path_pic, new_name))
        # 否则先转换CMYK
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(os.path.join(path_pic, new_name))
            pix0 = None
        newnamepathList.append(os.path.join(path_pic, new_name))
        # 释放资源
        pix = None
        print("提取了{}张图片".format(imgcount))
    return newnamepathList
def image2word(path):
    image = Image.open(path)
    text = pytesseract.image_to_string(image, lang='chi_sim')  # 使用简体中文解析图片
    #with open("output.txt", "w") as f:  # 将识别出来的文字存到本地
        #print(text)
        #f.write(text)
    return text

def pdf2word(path_pdf):
    path_temp = os.path.dirname(path_pdf)
    tempPicPathArray = pdf2image(path_pdf,path_temp)
    word = ''
    for picpath in tempPicPathArray:
        word += image2word(picpath)
#        if os.path.isfile(picpath):
#            os.remove(path)
    return word
if __name__=='__main__':
    # pdf路径
    path = r'D:\git\python_fgw\test\【徐发改投建〔2017〕3号】关于景东路（关港-闵行区界）辟通工程可行性研究报告的批复.pdf'
    # 创建保存图片的文件夹
    word = pdf2word(path)
    with open("output.txt", "w") as f:
        f.write(word)
#image2word("D_git_python_fgw_test_【徐发改核〔2019〕1】号漕河泾街道282c-01地块租赁住房新建项目.pdf_img1.png")

