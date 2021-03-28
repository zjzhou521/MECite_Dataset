#encoding:utf-8
import glob
import sys
import importlib
import os
importlib.reload(sys)
from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def get_file_name(path):
    i = 0
    name_flag = 0
    file_name = ""
    if(path[0] == '.'):
        i += 2
    while(i < len(path)):
        if(name_flag != 0):
            file_name += path[i]
        if(path[i] == '/'):
            name_flag = 1
        i += 1
    if('/' in file_name):
        return get_file_name(file_name)
    else:
        return file_name
def divide_file_name(name):
    i = 0
    before = ""
    after = ""
    divide_flag = 0
    while(i < len(name)):
        if(name[i] == '.'):
            divide_flag = 1
        if(divide_flag == 0):
            before += name[i]
        else:
            after += name[i]
        i += 1
    return before, after
def parse(input_path,output_path):
    """解析PDF文本，并保存到TXT文件中"""
    pdf_name_before, _ = divide_file_name(get_file_name(input_path))
    fp = open(input_path, 'rb')  # 'rb'表示解读为二进制数据
    #用文件对象创建一个PDF文档分析器
    parer = PDFParser(fp)
    #创建一个PDF文档
    doc = PDFDocument()
    #连接分析器，与文档对象--也就说内容与载体连接
    parer.set_document(doc)
    doc.set_parser(parer)

    #提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    #检测文档是否提供txt格式转化，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        #创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        #循环遍历列表，每次处理一个page内容
        #doc.get_pages() 获取pages列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            #接受该页面的LTPage对象
            layout = device.get_result()
            #这里layout是一个LTpage对象，里面存放着这个page解析出的各种对象
            #一般包括LTTextBox,LTFigure,LTImage,LTTextHorizontal等等
            #想要获得文本就获得对象的text属性
            for x in layout:
                if(isinstance(x, LTTextBoxHorizontal)):
                    with open(output_path+"/"+pdf_name_before+".txt", 'a', encoding='utf-8') as f:
                        results = x.get_text()
                       # return results
                        f.write(results+'\n')

# read pdfs
input_path = "./pdfs"
output_path = "./texts"
os.system("rm "+output_path+"/*")
pdfs = glob.glob("{}/*.pdf".format(input_path))
# convert to txt
fail_list = []
total_num = len(pdfs)
i = 0
for pdf in pdfs:
    i += 1
    print("[*] %d/%d:%s"%(i,total_num,pdf))
    try:
        parse(pdf, output_path)
    except:
        fail_list.append(pdf)
if(len(fail_list)!=0):
    with open(r"failed_pdfs.txt", 'a', encoding='utf-8') as f:
        # write failed pdf names
        sep = ';'
        f.write(sep.join(fail_list))
