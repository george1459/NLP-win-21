# Download all the PDF 

import os
import requests
from lxml import etree
import time
import traceback
from PyPDF2 import PdfFileReader

f=open("hrefs.txt","r",encoding="utf-8")
hrefs=eval(f.read())
f.close()
f=open("DOIs.txt","r",encoding="utf-8")
DOIs=eval(f.read())
f.close()
f=open("month_year.txt","r",encoding="utf-8")
month_year=eval(f.read())
f.close()

#input pdf file path 
def isValidPDF_pathfile(pathfile):
    bValid  =  True
    try :
        #PdfFileReader(open(pathfile, 'rb'))
        reader  =  PdfFileReader(pathfile)

        #check page numbers
        if  reader.getNumPages() <  1 :     
            bValid  =  False
    except :
        bValid  =  False

    return bValid

for i in range(len(hrefs)):

    dir_path=os.getcwd()+"\\"+month_year[i].split(" ")[0]+"-"+month_year[i].split(" ")[1]
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for j in range(len(DOIs[i])):
        name=month_year[i].split(" ")[0]+"-"+month_year[i].split(" ")[1]+"-"+DOIs[i][j].replace("/","")
        file_path=os.getcwd()+"\\"+month_year[i].split(" ")[0]+"-"+month_year[i].split(" ")[1]+"\\"+name+".pdf"
        if os.path.exists(file_path) and isValidPDF_pathfile(file_path):
            continue
        break1=0
        while 1:
            try:
                # supposed to use JSTOR but sci-hub is more straightforward

                res=requests.get("https://sci-hub.se/"+DOIs[i][j])
                if res.text.count("article not found")>0 or res.text.count("404 Not Found")>0:
                    time.sleep(2)
                    break1=1
                    break
                cmp=etree.HTML(res.text)
                href=cmp.xpath("//iframe[@id='pdf']/@src")[0]
                if href.count("http")==0:
                    href="http:"+href
                res=requests.get(href)
                break
            except Exception as e:
                continue
        if break1==1:
            continue
        print(DOIs[i][j])
        f=open(file_path, "wb")
        f.write(res.content)
        f.close()
        time.sleep(2)