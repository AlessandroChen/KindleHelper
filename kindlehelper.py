from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from Autopush import autopush
import os, stat

def addPermission(Filename):
    os.chmod(Filename, os.stat(Filename), st_mode | stat.S_IXUSR);

def transform(content):
    name = '';
    for i in range(0, len(content)):
        if (content[i] == ' ' and content[i + 1] == ' '):
            name += '\n';
        else:
            name += content[i];
    return name;

def getName(name):
    j = 0;
    for i in range(0, len(name)):
        if name[i:i+7] == 'content':
            j = i + 9;
            for j in range(i + 9, len(name)):
                if (name[j] == "'" or name[j] == '"'):
                    break;
            return name[i+9:j];


class ParseContent:
    def __init__(self, bookid):
        self.id = bookid;
        site = "https://www.booktxt.com/" + bookid + "/index.html"
        self.html = urlopen(site);
        self.bsObj = BeautifulSoup(self.html, features="html5lib");
        self.websites = [];
        self.chapter_name = [];
        self.shell = "pandoc -o "

    def parsehtml(self):
        for name in self.bsObj.findAll("meta", {"property":"og:novel:book_name"}):
            self.book_name = getName(repr(name));
        for name in self.bsObj.findAll("meta", {"property":"og:novel:author"}):
            self.author = getName(repr(name));
        for name in self.bsObj.findAll("meta", {"property":"og:novel:latest_chapter_name"}):
            self.last_chapter_name = getName(repr(name));
        for name in self.bsObj.findAll("meta", {"property":"og:image"}):
            self.image_url = getName(repr(name));

        # Download Cover Pic
        urlretrieve(self.image_url, 'cover.jpg');

        fi = open("title.txt", 'w');

        sign = '%'

        fi.write("%s %s\n%s %s\n" % (sign, self.book_name, sign, self.author));
        self.shell += self.book_name + ".epub" + " title.txt";

        for name in self.bsObj.find("div", {"id":"list"}).findAll("a"):
            Name = str(name.get_text());
            if ('第' in Name and '章' in Name):
                self.websites.append(name['href']);
                self.chapter_name.append(Name);

    def parsePage(self, num):
        site = "https://www.booktxt.com/" + self.id + self.websites[num - 1];
        html = urlopen(site);
        bsObj = BeautifulSoup(html, features="html5lib");
        fi = open(str(num) + '.md', 'w');
        self.shell += " " + str(num) + ".md";
        fi.write("## " + self.chapter_name[num - 1] + '\n\n');
        
        for name in bsObj.findAll("div", {"id":"content"}):
            Name = str(name).replace("<br>",'\n').replace("<br/>",'\n');
            fi.write(Name[19:-7]);
        fi.write('\n');

    def work(self):
        self.parsehtml();
        self.printInformation();

    def done(self, Filetype):
        self.shell += " --epub-cover-image=cover.jpg"
        if Filetype == '2':
            self.shell += " && kindlegen %s.mobi" % self.book_name;
        fi = open("translate.sh", "w");
        fi.write(self.shell);
        fe = open("clear.sh", "w");
        fe.write("rm *.md *.epub title.txt");
        addPermission("translate.sh");
        addPermission("clear.sh");
        print ("完成下载！");
        print ("正在为你转换 mobi 格式");
        os.system("./translate.sh");
        print ("正在推送");
        autopush.main_push(self.book_name);
        print ("可用 ./translate.sh 手动生成书籍")
        print ("可用 ./clear.sh 删除所有 md 文件");

    def printInformation(self):
        print ("书籍名称：", self.book_name);
        print ("最新章节：", self.last_chapter_name);
        print ("一共解析到", len(self.websites), "章");

def main():
    print ("请输入书籍编号 (www.booktxt.com)");

    bookid = input (">> ");

    print ("输入 1 以生成 epub 格式");
    print ("输入 2 以生成 mobi 格式");

    Filetype = input (">> ");


    content = ParseContent(bookid);
    content.work();

    st = input("请输入下载起始位置: ");
    ed = input("请输入下载结束位置: ");

    ed = min(int(ed), len(content.websites));

    for i in range(int(st), int(ed) + 1):
        print ("正在下载第 %04d 章" % i);
        content.parsePage(i);

    content.done(Filetype);

if __name__ == '__main__':
    main();
