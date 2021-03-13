# Convert pdf to jason

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import logging
import calendar

f=open("hrefs.txt","r",encoding="utf-8")
hrefs=eval(f.read())
f.close()
f=open("DOIs.txt","r",encoding="utf-8")
DOIs=eval(f.read())
f.close()
f=open("month_year.txt","r",encoding="utf-8")
month_year=eval(f.read())
f.close()

# show warning
logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)
device = PDFPageAggregator(PDFResourceManager(), laparams=LAParams())
interpreter = PDFPageInterpreter(PDFResourceManager(), device)

month_year_no=[]
DOIs_no=[]
texts=[]
for i in range(len(hrefs)):
    for j in range(len(DOIs[i])):
        name=month_year[i].split(" ")[0]+"-"+month_year[i].split(" ")[1]+"-"+DOIs[i][j].replace("/","")
        file_path="C:/Users/Administrator/Desktop/AER/extract/"+month_year[i].split(" ")[0]+"-"+month_year[i].split(" ")[1]+"/"+name+".pdf"
        if os.path.exists(file_path) and isValidPDF_pathfile(file_path):
            try:
                doc = PDFDocument()
                parser = PDFParser(open(file_path, 'rb'))
                parser.set_document(doc)
                doc.set_parser(parser)
                doc.initialize()

                # check if file can be coverted txt
                if not doc.is_extractable:
                    raise PDFTextExtractionNotAllowed
                else:
                    results=""
                    for page in doc.get_pages():
                        interpreter.process_page(page)
                     
                        # accept LTPage object
                        layout = device.get_result()
                        # Layout include LTPage objects 
                        # LTPage stores LTTextBox, LTFigure, LTImage, etc
                        # only need text
                      
                        for x in layout:
                            if isinstance(x, LTTextBoxHorizontal):
                                results += x.get_text().replace("\n","")
                    json1={}

                    # 1999年(march)3月
                    date1=month_year[i].split(" ")[1]+"年("+month_year[i].split(" ")[0]+")"+str(list(calendar.month_name).index(month_year[i].split(" ")[0]))+"月"
                    json1['date']=date1
                    json1['text']=results
                    json1['DOI']=DOIs[i][j]
                    texts.append(json1)

            except Exception as e:
                month_year_no.append(month_year[i])
                DOIs_no.append(DOIs[i][j])

f=open("texts_DOI.json","w",encoding="utf-8")
f.write(str(texts))
f.close()


# edits  
f = open("texts_DOI.jsonlist", 'w',encoding="utf-8")
for i in range(len(texts)):
    json1={}
    month=texts[i]['date'].split(")")[-1].replace("月","")
    if len(month)<2:
        month="0"+month
    json1["date"]=int(texts[i]['date'].split("年")[0]+month)
    json1["text"]=texts[i]['text']
    if len(json1["text"])=="":
        continue
    f.write(str(json1).replace('\'','\"')+"\n")
f.close()