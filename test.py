from bs4 import BeautifulSoup
import requests

html = requests.get('https://www.23us.la/html/443/443900/')
bsObj = BeautifulSoup(html.text, features = 'lxml')

from urllib.parse import urlparse
from urllib.parse import ParseResult
from urllib.parse import urlunparse

counter = 0

for tag in bsObj.findAll("a"):
        other = tag['href']
        o = urlparse(html.url)
        t = ParseResult(o.scheme, o.netloc, other, "","","")
        next_url = urlunparse(t)
        other_html = requests.get(next_url)
        print (other_html.text)
        break

