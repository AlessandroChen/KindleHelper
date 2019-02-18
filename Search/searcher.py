from urllib.request import quote
import requests

def get_book_link(book_name):
    book_name = quote(book_name.strip().encode('gbk'))
    html = requests.get("http://www.biquyun.com/modules/article/soshu.php?searchkey=" + repr(book_name)[1:-1])
    # print ("http://www.biquyun.com/modules/article/soshu.php?searchkey=" + repr(book_name)[1:-1])
    return html
