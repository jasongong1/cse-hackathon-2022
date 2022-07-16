import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from googlesearch import search

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
        return 0

# Search similar article by title
def searchArticlesByUrl(url):
    try:
        title = extractTitle(url)
        if (not title):
            return "extract title fail"
        domain = urlparse(url).netloc
        domain = removeLastChar('.', domain)
        query = f'{title} -inurl:{domain}'
        articles = []
        tmp = scrape_google(query)
        for item in tmp:
            articles.append(item)
        return articles
    except:
        return "error"

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

if __name__ == '__main__':
    url = 'https://www.nytimes.com/2022/07/15/us/politics/joe-manchin-senate-climate-tax.html'
    print(searchArticlesByUrl(url))
