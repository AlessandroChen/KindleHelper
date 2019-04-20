# Author: AlessandroChen
# IMPORT SECTION 
# from ... import ... as ...
from bs4 import BeautifulSoup as soup

from urllib.request import quote
import requests
import threading
import urllib3

from urllib.parse import urlparse
from urllib.parse import ParseResult
from urllib.parse import urlunparse

bookname = ''
index = 1
finished = 0

# CLASS SECTION

class Book:
    def __init__(self, book_url):
        self.chapter_name_list = []
        self.chapter_url_list = []
        self.section_name_list = []
        self.section_index_list = []
        self.origurl = book_url
        self.waiting_list = []

        self.orightml = requests.get(book_url)
        self.origbsObj = soup(self.orightml, features = 'lxml')

    def getChapterName(self, num):
        return self.chapter_name_list[num - 1]

    def parseOriginSite(self):
        '''
        '''
        html = requests.get(self.origurl)
        html.encoding = 'utf-8'
        bsObj = soup(html.text, features = 'lxml')
        
        self.writer = bsObj.find("a", {"class":"writer"}).get_text()

        global index

        for content in bsObj.findAll("div", {"class":"volume"}):
            self.section_index_list.append(index)
            section_name = content.h3.contents[2]
            self.section_name_list.append(section_name.strip())

            for chapter in content.findAll("a", {"class":""}):
                self.chapter_name_list.append(chapter.get_text().strip())
                # print (chapter.get_text())
                index += 1

        index -= 1

    def parseWebSite(self, siteurl, num):
        print ("parseWebSite(%s, %d)" % (siteurl, num))
        print ("Name: %s", self.chapter_name_list[num - 1])
        html = requests.get(siteurl, verify = False)
        if html.encoding == 'ISO-8859-1':
            html.encoding = 'utf-8'

        global finished
        finished += 1

    def downloadBook(self, start, end):

        search_html = BaiduSearch(bookname)
        search_bsObj = soup(search_html.text, features = 'lxml')

        self.waiting_list = [i for i in range(start, end + 1)]

        # 忽略 SSL Warning
        urllib3.disable_warnings()

        # threads = []

        for link in search_bsObj.findAll("h3", {"class":"t"}):
            '''
            先获取百度搜索内容
            然后爬取目录、进行所需筛选
            如果还有未成功的，继续向后爬取
            '''
            html = requests.get(link.a['href'], verify = False)
            html_encoding = html.encoding
            if html_encoding == 'ISO-8859-1':
                html.encoding = 'utf-8'
            bsObj = soup(html.text, features = 'lxml') # 获取目录页

            parse_html = urlparse(html.url)

            for target in self.waiting_list:
                print ("target = %d" % target)
                Chapter_inter_url = bsObj.find("a", string = self.chapter_name_list[target - 1])
                if Chapter_inter_url == None:
                    continue
                html_res = ParseResult(parse_html.scheme, parse_html.netloc, Chapter_inter_url['href'], "", "", "")
                site = urlunparse(html_res)
                # print (site)
                threading.Thread(target = self.parseWebSite, \
                                                args = (site, target,)).start()

        print ("finished")


# DECLARATION SECTION

BaiduUrl = 'http://www.baidu.com/s?wd='
QidianUrl = 'https://www.qidian.com/search?kw='
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# FUNCTIONS SECTION

def Help():
    print ("Usage:")
    print ("p 2    显示第二条对应章节")
    print ("d 1 2  下载第1至第2条对应章节")

def BaiduSearch(content):
    content = quote(content.strip().encode('gbk'))
    html = requests.get(BaiduUrl + repr(content)[1:-1])
    print (BaiduUrl + repr(content)[1:-1])
    html.encoding = 'utf-8'
    return html

def QidianSearch(book_name):
    book_name = quote(book_name.strip().encode('utf-8'))
    html = requests.get(QidianUrl + repr(book_name)[1:-1])
    html.encoding = 'utf-8'
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
    global bookname
    bookname = search_resname[int(resnum)]
    return book_url

# MAIN PROGRAM

def main():
    # book_name = input(">> 请输入书籍名称: ")

    # origin_site = QidianSearch(book_name)

    # newbook = Book(origin_site)

    newbook = Book('https://book.qidian.com/info/1012439051#Catalog')
    global bookname
    bookname = "哈利波特之血猎者"

    print ("正在解析 %s" % bookname)
    newbook.parseOriginSite()
    print ("解析完成，共解析到 %d 章" % index)

    while (1):
        prompt = input(">> ")
        prompt = prompt.strip().split()
        if (prompt[0] == 'p'):
            print (newbook.getChapterName(int(prompt[1])))
        elif (prompt[0] == 'd'):
            start = max(int(prompt[1]), 1)
            end = min(int(prompt[2]), index)
            newbook.downloadBook(start, end)
            return
        elif (prompt[0] == 'exit'):
            print ("Exit Successfully")
            return
        else:
            Help()

    return

if __name__ == '__main__':
    main()

