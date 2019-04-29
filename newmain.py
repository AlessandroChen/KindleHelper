# Author: AlessandroChen
# IMPORT SECTION 
# from ... import ... as ...
from bs4 import BeautifulSoup as soup

from urllib.request import quote
import requests, urllib3, os, re
import threading

from urllib.parse import urljoin

from goose3 import Goose
from goose3.text import StopWordsChinese

from selenium import webdriver
import time

firefox_option = webdriver.FirefoxOptions()
firefox_option.set_headless()


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
        self.trash_list = []

        self.orightml = requests.get(book_url)
        self.origbsObj = soup(self.orightml.text, features = 'lxml')

    def getChapterName(self, num):
        return self.chapter_name_list[num - 1]

    def parseOriginSite(self):
        eng = webdriver.Firefox(options = firefox_option)
        # eng.implicitly_wait(5)
        eng.get(self.origurl)
        time.sleep(3)
        bsObj = soup(eng.page_source, features = 'lxml')

        print ("解析完成")
        
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
        print ("Name: ", self.chapter_name_list[num - 1])
        content = ''
        g = Goose({'stopwords_class': StopWordsChinese})
        print ("Goose ", siteurl)
        try:
            article = g.extract(url = siteurl)
            content = article.cleaned_text
            if (content == ''):
                return 
            with open("%d.md" % num, 'w') as f:
                f.write("## %s\n\n" % self.chapter_name_list[num])
                f.write(content)
            # print (siteurl, num)
            # print ("aritcle", article.title)
        except:
            return False
        
        global finished
        finished += 1
        # self.waiting_list.remove(num)
        self.trash_list.append(num)
        return True


    def downloadBook(self, start, end):

        try:
            os.mkdir(bookname)
        except:
            print ("Dir exist!")
        os.chdir(bookname)

        search_html = BaiduSearch(bookname)
        search_bsObj = soup(search_html.text, features = 'lxml')

        self.waiting_list = [i for i in range(start, end + 1)]

        # 忽略 SSL Warning
        urllib3.disable_warnings()

        # threads = []

        for link in search_bsObj.findAll("h3", {"class":"t"}):
            failed_times = 0
            if len(self.waiting_list) == 0: # Finished
                break
            try:
                html = requests.get(link.a['href'], verify = False)
            except:
                continue
            html_encoding = html.encoding
            if html_encoding == 'ISO-8859-1':
                html.encoding = 'utf-8'
            bsObj = soup(html.text, features = 'lxml') # 获取目录页

            for target in self.waiting_list:
                Chapter_inter_url = bsObj.find("a", string = self.chapter_name_list[target - 1])
                if Chapter_inter_url == None:
                    failed_times += 1
                    print (self.chapter_name_list[target - 1], "not found")
                    print (html.url)
                    if failed_times >= 10:
                        break
                    continue
                print ('\n'*2)
                print ("target = %d" % target)
                print ("Before Join ", html.url, Chapter_inter_url['href'])
                site = urljoin(html.url, Chapter_inter_url['href'])
                print ("After :", site)
                # threading.Thread(target = self.parseWebSite, \
                #                 args = (site, target ,)).start()
                if self.parseWebSite(site, target) == False:
                    break

            for trash_num in self.trash_list:
                self.waiting_list.remove(trash_num)

        print (self.waiting_list)
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
    isTest = 0
    if isTest == 0:
        book_name = input(">> 请输入书籍名称: ")
        origin_site = QidianSearch(book_name)
        newbook = Book(origin_site)
    else:
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

