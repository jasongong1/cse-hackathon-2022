from pandas import read_csv
from urllib import parse


# Given a full URL, finds the reliability and bias ratings for that url and returns them as a tuple (reliability, bias) 
def returnBias(url):

    hostname = (parse.urlsplit(url)[1])[4:]

    data = read_csv('media_bias_chart_urls.csv')

    if data['URL'].str.contains(hostname).any():
        index = data.index[data['URL']==hostname].to_list()
        print((data['Vertical Rank'][index[0]], data['Horizontal Rank'][index[0]]))
        return((data['Vertical Rank'][index[0]], data['Horizontal Rank'][index[0]]))
        

returnBias("http://www.axios.com")