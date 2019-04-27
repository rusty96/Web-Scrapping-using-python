from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd

pages = np.arange(1, 9951, 50) #can only go to 10000 items because after that the URI ha no discernable distinction
#initialize empty lists to store the variables scraped
titles = []
years = []
ratings = []
genres = []
runtimes = []
imdb_ratings = []
metascores = []
votes = []
for page in pages:

    #get request
    response = get("https://www.imdb.com/search/title?genres=sci-fi&"
                   + "start="
                   + str(page)
                   + "&explore=title_type,genres&ref_=adv_prv")

    sleep(randint(8,15))

    #throw warning for status codes that are not 200
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    #parse the content of current iteration of request
    page_html = BeautifulSoup(response.text, 'html.parser')

    movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

    #extract the 50 movies for that page
    for container in movie_containers:

        #conditional for all with metascore
        if container.find('div', class_ = 'ratings-metascore') is not None:

            #title
            title = container.h3.a.text
            titles.append(title)

            #year released
            year = container.h3.find('span', class_= 'lister-item-year text-muted unbold').text
            years.append(year)

            #rating
            rating = container.p.find('span', class_= 'certificate').text
            ratings.append(rating)

            #genre
            genre = container.p.find('span', class_ = 'genre').text
            genres.append(genre)

            #runtime
            time = container.p.find('span', class_ = 'runtime').text
            runtimes.append(time)

            #IMDB ratings
            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)

            #Metascore
            m_score = container.find('span', class_ = 'metascore').text
            metascores.append(int(m_score))

            #Number of votes
            vote = container.find('span', attrs = {'name':'nv'})['data-value']
            votes.append(int(vote))
