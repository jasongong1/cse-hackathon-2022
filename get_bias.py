from pandas import read_csv
from urllib import parse

def returnBias(url):

    hostname = (parse.urlsplit(url)[1])[4:]

    data = read_csv('media_bias_chart_urls.csv')

    if data['URL'].str.contains(hostname).any():
        index = data.index[data['URL']==hostname].to_list()
        print((data['Vertical Rank'][index[0]], data['Horizontal Rank'][index[0]]))
        return((data['Vertical Rank'][index[0]], data['Horizontal Rank'][index[0]]))
        

returnBias("http://www.axios.com")