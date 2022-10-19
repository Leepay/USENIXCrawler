from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
import os
from multiprocessing import Pool

url = 'https://www.usenix.org/conference/usenixsecurity22/summer-accepted-papers'
flag = "/conference/usenixsecurity22/presentation/"
pdf_rule = "https://www.usenix.org/system/files/sec22-"
process_num = 7

def downloadPDF(tag):
    os.system("wget -P /home/liulp/Project/USENIX_CRAWLER/summer " + pdf_rule + tag + '.pdf')
    print(tag+' Done')

if __name__ == '__main__':
    # 获取每篇paper的id(tag)
    wb_data = requests.get(url)
    soup = str(BeautifulSoup(wb_data.content,"lxml"))
    tag_list = []
    for line in soup.split('\n'):
        if flag in line:
            paper_tag = line[line.find(flag)+len(flag):].split('\"')[0]
            if paper_tag not in tag_list:
                tag_list.append(paper_tag)
    with Pool(process_num) as p:
        p.map(downloadPDF,tag_list)