import requests
import config
from bs4 import BeautifulSoup
import csv

list_headers = ['Movie_Id','title', 'year','genre','rating','count']
title = []
year = []
genre = []
rating = []
count = []

def text_to_num(text):
    d = {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000
    }
    if text[-1] in d:
        # separate out the K, M, or B
        num, magnitude = text[:-1], text[-1]
        return int(float(num) * d[magnitude])
    else:
        return float(text)


def write_data(file_name, title, year, genre, rating, count):
    with open(file_name,'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(list_headers)
        for i in range(len(title)):
            writer.writerow([i+1,title[i],year[i],genre[i],rating[i],count[i]])
        


def cards_url():
    response = requests.get(config.databaseurl_Movies)
    soup = BeautifulSoup(response.text,'lxml')
    data = soup.find_all('td', class_="titleColumn")

    for i in data:
        card_url = 'https://www.imdb.com'+ i.find('a').get('href')
        yield card_url

i = 0
for movie_url in cards_url():
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.find('h1', class_ = 'sc-b73cd867-0 eKrKux'):
        title.append(soup.find('h1', class_ = 'sc-b73cd867-0 eKrKux').text)
        year.append(soup.find('span', class_ = 'sc-8c396aa2-2 itZqyK').text)
        genre.append(soup.find('span', class_ = 'ipc-chip__text').text)
        rating.append(soup.find('span', class_ = 'sc-7ab21ed2-1 jGRxWM').text)
        count.append(text_to_num(soup.find('div', class_ = 'sc-7ab21ed2-3 dPVcnq').text))
        print(i)
        i+=1

write_data(config.data_csv_num,title,year,genre,rating,count)   