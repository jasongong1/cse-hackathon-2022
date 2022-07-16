from pandas import read_csv
from urllib import parse


# Given a full URL, finds the reliability and bias ratings for that url and returns them as a tuple (reliability, bias) 
def returnBias(url):

    hostname = (parse.urlsplit(url)[1])[4:]

    data = read_csv('media_bias_chart_urls.csv')

    for idx, knownHost in enumerate(data['URL']):
        if knownHost in hostname:
            return((data['Vertical Rank'][idx], data['Horizontal Rank'][idx]))


# STOP GOLFING!
    # if data['URL'].str.contains(hostname).any():
    #     index = data.index[data['URL']==hostname].to_list()
    #     if (len(index) == 0):
    #         return ((100, 100))
    #     return((data['Vertical Rank'][index[0]], data['Horizontal Rank'][index[0]]))
    # else:
    #     return 0

# convert the bias value given by returnBias to a string representing the level of bias
def biasToString(bias):
    if bias < -30:
        return "Very Strongly Left"
    elif bias < -18:
        return "Strongly Left"
    elif bias < -6:
        return "Moderately Left"
    elif bias < -2:
        return "Slightly Left"
    elif bias < 2:
        return "Neutral"
    elif bias < 6:
        return "Slightly Right"
    elif bias < 18:
        return "Moderately Right"
    elif bias < 30:
        return "Strongly Right"
    elif bias < 42:
        return "Very Strongly Right"

# convert the reliability value given by returnBias to a string representing the level of fact reporting
def reliabilityToString(rel):
    if rel < 8:
        return "Inaccurate/Fabricated"
    elif rel < 24:
        return "Misleading/Selective"
    elif rel < 48:
        return "Variable, Some Factual Reporting"
    elif rel < 56:
        return "Factual Reporting"
    elif rel < 64:
        return "Original Factual Reporting"

if __name__=="__main__":
    bias = returnBias("http://www.axios.com")
    print(bias)
    print(reliabilityToString(bias[0]))
    print(biasToString(bias[1]))
    print(returnBias("https://www.theguardian.com/australia-news/2022/jul/16/anthony-albanese-reverses-decision-to-scrap-pandemic-leave-payments-after-national-cabinet-meets"))