from bs4 import BeautifulSoup as soup
from Autopush import autopush
from Config import config
from progressbar import *
from Functions import parsetool
import requests
import os, stat, glob
import threading

ParseSite = 'http://www.biquyun.com/'

class ParseContent:
    def __init__(self, book_id):
        self.id = book_id
        self.chapter_link = []
        self.chapter_name = []
        self.shell = "pandoc -o "

        self.html = requests.get(ParseSite + book_id)
        self.html.encoding = 'gbk'
        self.bsObj = soup(self.html.text, features = "lxml")

    def parsehtml(self):
        print ("正在解析目录");
        for content in self.bsObj.findAll("meta", {"property":"og:novel:book_name"}):
            self.book_name = parsetool.getContent(repr(content))
            print (self.book_name);
        for content in self.bsObj.findAll("meta", {"property":"og:novel:author"}):
            self.author = parsetool.getContent(repr(content))
        for content in self.bsObj.findAll("meta", {"property":"og:novel:latest_chapter_name"}):
            self.latest_chapter_name = parsetool.getContent(repr(content))

        # 生成名称、作者页面
        Book_info_file = open("title.txt", 'w')
        sign = '%'
        Book_info_file.write("%s %s\n%s %s\n" % (sign, self.book_name, sign, self.author))
        Book_info_file.close();

        for chapter_links in self.bsObj.find("div", {"id":"list"}).findAll("a"):
            Name = str(chapter_links.get_text())
            if ('第' in Name and '章' in Name):
                self.chapter_link.append(chapter_links['href'])
                self.chapter_name.append(Name)

        if len(self.chapter_link) == 0:
            # 不是 "第 章" 形式
            for chapter_links in self.bsObj.find("div", {"id":"list"}).findAll("a"):
                self.chapter_link.append(chapter_links['href'])
                self.chapter_name.append(Name)

    def parsePage(self, num):
        site = ParseSite + self.chapter_link[num - 1]
        html = requests.get(site)
        html.encoding = 'gbk'
        bsObj = soup(html.text, features="lxml")
        fi = open(str(num) + '.md', 'w')
        fi.write("## " + self.chapter_name[num - 1] + '\n\n')
        
        for name in bsObj.findAll("div", {"id":"content"}):
            Name = str(name).replace("<br>",'\n').replace("<br/>",'\n')
            fi.write(Name[19:-7])
        fi.write('\n')

    def work(self):
        self.parsehtml()
        self.printInformation()

    def done(self, Filetype, st, ed):
        # 生成脚本
        print ("正在生成脚本...");
        self.shell += self.book_name + ".epub" + " title.txt"
        for i in range(int(st), int(ed) + 1):
            self.shell += " " + str(i) + ".md"
        if Filetype == '2':
            self.shell += " && kindlegen %s.epub" % self.book_name
        fi = open("translate.sh", "w")
        fi.write(self.shell)
        fi.close()
        fe = open("clear.sh", "w")
        fe.write("rm *.md *.epub title.txt")
        fe.close()
        parsetool.addPermission("translate.sh")
        parsetool.addPermission("clear.sh")
        print ("正在为你转换 mobi 格式")
        os.system("./translate.sh")
        print ("正在推送")
        en = autopush.emailSender()
        en.sendEmailWithAttr(config.receiver,config.username,config.password,"%s.mobi" % self.book_name)
        print ("可用 ./translate.sh 手动生成书籍")
        print ("可用 ./clear.sh 删除所有 md 文件")

    def printInformation(self):
        print ("="*40)
        print ("书籍名称：", self.book_name)
        print ("最新章节：", self.latest_chapter_name)
        print ("一共解析到", len(self.chapter_link), "章")
        print ("="*40)

def main():
    print ("请输入书籍编号 (www.biquyun.com)")

    book_id = input (">> ")

    print ("输入 1 以生成 epub 格式")
    print ("输入 2 以生成 mobi 格式")

    Filetype = input (">> ")

    content = ParseContent(book_id)
    content.work()

    st = input("请输入下载起始位置: ")
    ed = input("请输入下载结束位置: ")

    ed = min(int(ed), len(content.chapter_link))

    threads = []

    for i in range(int(st), int(ed) + 1):
        t = threading.Thread(target = content.parsePage, args = (i,))
        threads.append(t)


    total = int(ed)-int(st)
    psb = ProgressBar().start()

    for t in threads:
        psb.update(int(len(glob.glob(pathname="*.md")) / total * 100));
        t.start()
        while 1:
            psb.update(int(len(glob.glob(pathname="*.md")) / total * 100));
            if (len(threading.enumerate()) < 600):
                break;

    while (len(threading.enumerate()) >= 2):
        psb.update(int(len(glob.glob(pathname="*.md")) / total * 100));

    for t in threads:
        t.join()

    psb.finish();
    print ("完成下载!");

    content.done(Filetype, st, ed)

if __name__ == '__main__':
    main()
