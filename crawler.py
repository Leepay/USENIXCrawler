from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

def craw(season):
    url = 'https://www.usenix.org/conference/usenixsecurity22/'+season+'-accepted-papers'
    flag = "/conference/usenixsecurity22/presentation/"
    summary_file = '汇总文件_'+season+'.xlsx'

    # 获取每篇paper的id(tag)
    wb_data = requests.get(url)
    soup = str(BeautifulSoup(wb_data.content,"lxml"))
    tag_list = []
    for line in soup.split('\n'):
        if flag in line:
            paper_tag = line[line.find(flag)+len(flag):].split('\"')[0]
            if paper_tag not in tag_list:
                tag_list.append(paper_tag)
    excel_file = Workbook()
    excel_sheet = excel_file.active
    excel_sheet.title = 'Sheet1'
    excel_sheet.append(['tag','标题','摘要'])
    cnt = 0
    for i_tag in tag_list:
        cnt += 1
        try:
            wb_data = requests.get("https://www.usenix.org//conference/usenixsecurity22/presentation/"+i_tag)
        except:
            continue
        soup = BeautifulSoup(wb_data.content, "lxml")
        title = str(soup.select('h1'))[21:-6]
        print(str(cnt)+' '+title)
        paragraphs = soup.find_all(name='div',attrs={"class":"field-item odd"})
        abstract_p = paragraphs[1].select('p')
        abstract = "\n".join([str(i_paragraph.string) for i_paragraph in abstract_p])
        # print(abstract)
        excel_sheet.append([i_tag,title,abstract])
    excel_file.save(filename=summary_file)

if __name__ == '__main__':
    craw('summer')
    craw('fall')
    craw('winter')