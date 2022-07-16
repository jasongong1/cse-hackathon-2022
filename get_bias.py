from pandas import read_csv


def returnBias(url):

    data = read_csv('media_bias_chart_urls.csv')

    if url in data['URL']:
        print((['Vertical Rank'], data['Horizontal Rank']))

    # with open('media_bias_chart_urls.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
        

returnBias("http://www.cnn.com")