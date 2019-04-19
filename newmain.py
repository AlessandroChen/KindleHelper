# Author: AlessandroChen
# IMPORT SECTION 
# from ... import ... as ...
from bs4 import BeautifulSoup as soup

from urllib.request import quote
import requests

# CLASS SECTION

class Book:
    def __init(self, book_url):
        self.chapter_name = []
        self.chapter_url = []

# DECLARATION SECTION

BaiduUrl = 'https://www.baidu.com/s?wd='
QidianUrl = 'https://www.qidian.com/search?kw='
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# FUNCTIONS SECTION

def BaiduSearch(content):
    content = quote(content.strip().encode('gbk'))
    html = requests.get(BaiduUrl + repr(content)[1:-1])
    return html

def QidianSearch(book_name):
    book_name = quote(book_name.strip().encode('utf8'))
    html = requests.get(QidianUrl + repr(book_name)[1:-1])
    html.encoding = 'utf8'
    bsObj = soup(html.text, features = 'lxml')
    search_resname = []
    search_resurl = []
    for search_res in bsObj.findAll("h4"):
        search_resname.append(search_res.get_text())
        # print (search_res.contents[0]['href'])
        search_resurl.append(search_res.contents[0]['href'])
    for num, sname in enumerate(reversed(search_resname)):
        print ("\033[1;35m [%02d] \033[0m %s" % (len(search_resname) - num - 1, sname))
    resnum = input(">> 请选择结果: ")
    book_url = 'https:' + search_resurl[int(resnum)] + '#Catalog';
    return book_url

# MAIN PROGRAM

def main():
    book_name = input(">> 请输入书籍名称: ")

    origin_site = QidianSearch(book_name)

    return

if __name__ == '__main__':
    main()

