# parseSite = 'http://www.quanshuwang.com'

from bs4 import BeautifulSoup as soup
from urllib.request import quote
import requests

catelog_url = ''

def search_book_url(book_name):
    book_name = quote(book_name.strip().encode('gbk'))
    html = requests.get("http://www.quanshuwang.com/modules/article/search.php?searchkey=%s&searchtype=articlename&searchbuttom.x=0&searchbuttom.y=0" % repr(book_name)[1:-1])
    html.encoding = 'gbk'
    bsObj = soup(html.text, features = 'lxml')
    global catelog_url
    catelog_url = bsObj.find("a", {"class":"reader"})['href']
    # print (catelog_url)

def parse_book_catelog():
    html = requests.get(catelog_url)
    html.encoding = 'gbk'
    bsObj = soup(html.text, features = 'lxml')

    for chapter_links in self.bsObj.find("div", {"class":"clearfix dirconone"}).findAll("a"):
        Name = str(chapter_links.get_text())
        chapter_link.append(chapter_links['href'])
        chapter_name.append(Name)
