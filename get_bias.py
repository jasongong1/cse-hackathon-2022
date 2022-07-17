from pandas import read_csv
from urllib import parse


# Given a full URL, finds the reliability and bias ratings for that url and returns them as a tuple (reliability, bias) 
def returnBias(url):

    hostname = (parse.urlsplit(url)[1])[4:]

    data = read_csv('media_bias_chart_urls.csv')

    for idx, knownHost in enumerate(data['URL']):
        if knownHost in hostname:
            return((data['Vertical Rank'][idx], data['Horizontal Rank'][idx], data['News Source'][idx]))


# STOP GOLFING!
    # if data['URL'].str.contains(hostname).any():
    #     index = data.index[data['URL']==hostname].to_list()
    #     if (len(index) == 0):
    #         return ((100, 100))
    #     return((data['Vertical Rank'][index[0]], data['Horizontal Rank'][index[0]]))
    # else:
    #     return 0

def biasToIdx(bias):
    if bias < -30:
        return 0
    elif bias < -18:
        return 1
    elif bias < -6:
        return 2
    elif bias < -2:
        return 3
    elif bias < 2:
        return 4
    elif bias < 6:
        return 5
    elif bias < 18:
        return 6
    elif bias < 30:
        return 7
    elif bias < 42:
        return 8


def reliabilityToIdx(rel):
    if rel < 8:
        return 0
    elif rel < 24:
        return 1
    elif rel < 48:
        return 2
    elif rel < 56:
        return 3
    elif rel < 64:
        return 4

if __name__=="__main__":
    bias = returnBias("http://www.axios.com")
    print(bias)
    print(reliabilityToString(bias[0]))
    print(biasToString(bias[1]))
    print(returnBias("https://www.theguardian.com/australia-news/2022/jul/16/anthony-albanese-reverses-decision-to-scrap-pandemic-leave-payments-after-national-cabinet-meets"))