# Author: AlessandroChen
# IMPORT SECTION 
# from ... import ... as ...
from bs4 import BeautifulSoup as soup

from urllib.request import quote
import requests
import threading

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

    def getChapterName(self, num):
        return self.chapter_name_list[num - 1]

    def parseOriginSite(self):
        '''
        '''
        html = requests.get(self.origurl)
        html.encoding = 'utf8'
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

    def parseWebSite(self, num):
        print ("parse %d" % num)
        finished += 1
        pass

    def downloadBook(self, start, end):
        threads = []
        for i in range(start, end):
            threads.append(threading.Thread(target = self.parseWebSite, args = (i,)))

        for t in threads:
            t.start()


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
    global bookname
    bookname = search_resname[int(resnum)]
    return book_url

# MAIN PROGRAM

def main():
    # book_name = input(">> 请输入书籍名称: ")

    # origin_site = QidianSearch(book_name)

    # newbook = Book(origin_site)

    newbook = Book('https://book.qidian.com/info/1012439051#Catalog')

    print ("正在解析 %s" % bookname)
    newbook.parseOriginSite()
    print ("解析完成，共解析到 %d 章" % index)

    while (1):
        prompt = input(">> ")
        prompt = prompt.strip().split()
        if (prompt[0] == 'l'):
            print (newbook.getChapterName(int(prompt[1])))
        elif (prompt[0] == 'd'):
            start = max(int(prompt[1]), 1)
            end = min(int(prompt[2]), index)
            newbook.downloadBook(start, end)
        elif (prompt[0] == 'exit'):
            print ("Exit Successfully")
            return
        else:
            pass

    return

if __name__ == '__main__':
    main()

