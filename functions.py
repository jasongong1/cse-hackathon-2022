import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import get_bias

from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from googlesearch import search
#from readability.readability import Document

def removeLastChar(elem, arr):
    index_pos = len(arr) - arr[::-1].index(elem) - 1
    return arr[:index_pos]

# Extract title from url
def extractTitle(url):
    #try:
    fileObj = urlopen(url)
    html = fileObj.read()
    title = BeautifulSoup(html, 'html.parser').title.text
    #title = removeLastChar('-', title)
    return title
    #except:
    #    return 0

# Search similar article by title
def searchArticlesByUrl(url):
    try:
        title = extractTitle(url)
        if (title == "error"):
            return "error1"
        domain = urlparse(url).netloc
        domain = removeLastChar('.', domain)
        query = f'{title} -inurl:{domain}'
        articles = []
        tmp = scrape_google(query+"article", url)
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

def scrape_google(query, original_url):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.' ,
                      'https://www.youtube.')

    for url in links[:]:
        if url.startswith(google_domains) or url == original_url:
            links.remove(url)

    return links


# main function called by web frontend
def returnBiases(url):
    out = []
    articles = searchArticlesByUrl(url)
    for article in articles:
        art = {}
        bias = get_bias.returnBias(article)
        if not bias:
            continue
        art['url'] = article
        art['Accuracy'] = get_bias.reliabilityToString(bias[0])
        art['Bias'] = get_bias.biasToString(bias[1])
        out.append(art)
    return out

if __name__ == '__main__':
    #url = 'https://www.bbc.com/news/world-europe-62189272'
    #url = "https://www.nytimes.com/2022/07/15/us/politics/joe-manchin-senate-climate-tax.html"
    #url = "https://www.theguardian.com/us-news/2022/jul/15/ivana-trump-donald-trump-wife-death-cause"

    #url = "https://www.msnbc.com/rachel-maddow-show/maddowblog/republicans-balk-bill-protect-interstate-abortion-travel-rcna38404"
    url = "https://www.washingtonpost.com/politics/2022/07/15/secret-service-subpoena-erased-texts/"


    #print(extractTitle(url))
    #print(searchArticlesByUrl(url))
    print(returnBiases(url))