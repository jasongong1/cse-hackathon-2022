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
        
        print("hi")
    #title = removeLastChar('-', title)
    #print(title)
    return title
    #except:
    #    return 0

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
            art['url'] = article
            art['title'] = extractTitle(article)
            art['Accuracy'] = get_bias.reliabilityToString(bias[0])
            art['Accuracy_num'] = int(bias[0])
            art['Bias'] = get_bias.biasToString(bias[1])
            art['source'] = bias[2]
            out.append(art)

    # sort
    out = sorted(out, key=lambda d: d['Accuracy_num'], reverse=True) 

    # add original article to output
    art = {}
    bias = get_bias.returnBias(url)
    if not bias:
        return out
    art['url'] = url
    art['title'] = extractTitle(url)
    art['Accuracy'] = get_bias.reliabilityToString(bias[0])
    art['Accuracy_num'] = int(bias[0])
    art['Bias'] = get_bias.biasToString(bias[1])
    out.insert(0,art)

    #return out[1:] if out else []
    return out

if __name__ == '__main__':
    #url = 'https://www.bbc.com/news/world-europe-62189272'
    #url = "https://www.nytimes.com/2022/07/15/us/politics/joe-manchin-senate-climate-tax.html"
    #url = "https://www.theguardian.com/us-news/2022/jul/15/ivana-trump-donald-trump-wife-death-cause"

    #url = "https://www.msnbc.com/rachel-maddow-show/maddowblog/republicans-balk-bill-protect-interstate-abortion-travel-rcna38404"
    url = "https://www.washingtonpost.com/politics/2022/07/15/secret-service-subpoena-erased-texts/"


    print(extractTitle("https://www.wsj.com/articles/jan-6-committee-subpoenas-secret-service-for-deleted-text-messages-11657943958"))
    #print(searchArticlesByUrl(url))
    #print(returnBiases(url))