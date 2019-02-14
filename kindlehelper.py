from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

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

        fi = open("tititle.txt", 'w');

        sign = '%'

        fi.write("%s %s\n%s %s\n" % (sign, self.book_name, sign, self.author));
        self.shell += self.book_name + ".epub" + " tititle.txt";

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
        
        # for name in bsObj.findAll("br"):
            # fi.write(transform(name.get_text()) + '\n');
        for name in bsObj.findAll("div", {"id":"content"}):
            Name = str(name).replace("<br>",'\n').replace("<br/>",'\n');
            fi.write(Name[19:-7]);
        fi.write('\n');

    def work(self):
        self.parsehtml();
        self.printInformation();

    def done(self):
        self.shell += " --epub-cover-image=cover.jpg"
        fi = open("translate.sh", "w");
        fi.write(self.shell);

    def printInformation(self):
        print (self.book_name);
        print (self.last_chapter_name);
        print (len(self.websites));

def main():
    print ("Please Enter Book Id from www.booktxt.com:");

    bookid = input (">> ");

    content = ParseContent(bookid);
    content.work();

    st = input("Start From: ");
    ed = input("End At: ");

    ed = min(int(ed), len(content.websites));

    for i in range(int(st), int(ed) + 1):
        print ("i = %d" % i);
        content.parsePage(i);

    content.done();


if __name__ == '__main__':
    main();
