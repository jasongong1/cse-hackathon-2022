from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from googlesearch import search
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}

def removeLastChar(elem, arr):
    index_pos = len(arr) - arr[::-1].index(elem) - 1
    return arr[:index_pos]

# Extract title from url
def extractTitle(url):
    try:
        fileObj = urlopen(url)
        html = fileObj.read()
        title = BeautifulSoup(html, 'html.parser').title.text
        title = removeLastChar('-', title)
        return title
    except:
        return "error"

# Search similar article by title
def searchArticlesByTitle(url):
    try:
        title = extractTitle(url)
        if (title == "error"):
            return "error"
        domain = urlparse(url).netloc
        domain = removeLastChar('.', domain)
        query = f'{title} -inurl:{domain}'
        articles = list()
        for item in search(query, num=30, stop=30, pause=2):
            articles.append(item)
        return articles
    except:
        return "error"


if __name__ == '__main__':
    url = 'https://www.bbc.com/news/world-europe-62189272'
    print(extractTitle(url))
    print(searchArticlesByTitle(url))
