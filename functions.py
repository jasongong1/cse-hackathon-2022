import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import get_bias

import yake

kw_extractor = yake.KeywordExtractor(lan="en",n=2,dedupLim=0.5,top=8)

from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#from readability.readability import Document

biasStrList = [
    "Very Strongly Left",
    "Strongly Left",
    "Moderately Left",
    "Slightly Left",
    "Neutral",
    "Slightly Right",
    "Moderately Right",
    "Strongly Right",
    "Very Strongly Right"
]

biasColorList = [
    "#2f2bab",
    "#5854b8",
    "#8684c4",
    "#cbc9f0",
    "#fff",
    "#ffd7d4",
    "#ffaea8",
    "#e35146",
    "#c9190c"
]

reliabilityStrList = [
    "Inaccurate/Fabricated",
    "Misleading/Selective",
    "Some Factual Reporting",
    "Factual Reporting",
    "Highly Factual Reporting"
]

reliabilityColorList = [
    "#fff",
    "#a5f0c4",
    "#3db36d",
    "#69c990",
    "#109c4a"
]


def removeLastChar(elem, arr):
    index_pos = len(arr) - arr[::-1].index(elem) - 1
    return arr[:index_pos]

# Extract title from url
def extractTitle(url):
    #try:
    # fileObj = urlopen(url)
    # html = fileObj.read()
    # title = BeautifulSoup(html, 'html.parser').select('h1.listing-name')[0].text.strip()

    
    req_from_url = requests.get(url)
    text_from_req = req_from_url.text
    print(url)
    try:
        titles = BeautifulSoup(text_from_req, 'html.parser')
        title = titles.select('h1')[0].text.strip()
        if "404" in title:
            return url
        print(title)
    except:
        return url
    return title

# Search similar article by title
def searchArticlesByUrl(url):
    try:
        title = extractTitle(url)

        kw_list = extractKeywords(title)
        
        if (title == "error"):
            return "error1"

        domain = urlparse(url).netloc
        domain = removeLastChar('.', domain)

        query = ""

        for kw in kw_list:
            query += kw[0] + " "

        query += f"-inurl:{domain}"

        print(query)

        articles = []
        for item in scrape_google(query, url):
            articles.append(item)
        return articles
    except:
        return "error"

def extractKeywords(titleStr):
    kw_list = kw_extractor.extract_keywords(titleStr)
    print(kw_list)
    return kw_list

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
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.' ,
                      'https://www.youtube.')


    newlinks = []

    for url in links:
        if (url.startswith(google_domains)
            or url == original_url
            or any(dm in url for dm in google_domains)):
            continue
        newlinks.append(url)
    return newlinks


# main function called by web frontend
def returnBiases(url):
    out = []
    articles = searchArticlesByUrl(url)

    print(articles)

    # add searched articles to output
    for article in articles:
        art = {}
        bias = get_bias.returnBias(article)
        if bias:
            relIdx = get_bias.reliabilityToIdx(bias[0])
            biasIdx = get_bias.biasToIdx(bias[1])
            art['url'] = article
            art['Accuracy'] = reliabilityStrList[relIdx]
            art['accuracy_color'] = reliabilityColorList[relIdx]
            art['title'] = extractTitle(article)
            art['Accuracy_num'] = int(bias[0])
            art['Bias'] = biasStrList[biasIdx]
            art['bias_color'] = biasColorList[biasIdx]
            art['source'] = bias[2]
            out.append(art)

    # sort
    out = sorted(out, key=lambda d: d['Accuracy_num'], reverse=True) 

    # add original article to output
    art = {}
    bias = get_bias.returnBias(url)
    if not bias:
        return out

    relIdx = get_bias.reliabilityToIdx(bias[0])
    biasIdx = get_bias.biasToIdx(bias[1])

    art['url'] = url
    art['Accuracy'] = reliabilityStrList[relIdx]
    art['accuracy_color'] = reliabilityColorList[relIdx]
    art['title'] = extractTitle(url)
    art['Accuracy_num'] = int(bias[0])
    art['Bias'] = biasStrList[biasIdx]
    art['bias_color'] = biasColorList[biasIdx]
    art['source'] = bias[2]
    out.insert(0,art)
    return out