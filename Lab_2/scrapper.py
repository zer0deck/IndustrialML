# -*- coding: utf-8 -*-

"""
This is IMDB scrapper, scrapping movies data, including poster and short description.
Instead of using strange IMDB API, we decided to use our oun scrapper.
"""

import re
import time
import random
import requests
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
# from translate import Translator

if __name__=="__main__":
    df = pd.read_csv('Lab_2/data.csv', sep=';', encoding='utf-8')
    # translator= Translator(from_lang="russian", to_lang="english")
    genres = ['Romance', 'Sci-Fi', 'Short', 'Sport', 'Superhero', 'Thriller', 'War', 'Western', 'Documentary']
    # genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Superhero', 'Thriller', 'War', 'Western', 'Documentary']
    for i in range(15, 21, 5):
        for genre in genres:
            if genre == 'Superhero':
                url = f'https://www.imdb.com/search/title/?title_type=feature&genres={genre}&start={i}1&explore=genres&ref_=adv_explore_rhs'
            else:
                url = f'https://www.imdb.com/search/title/?genres={genre}&start={i}1&explore=genres&ref_=adv_explore_rhs'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            movies = soup.select('h3.lister-item-header')
            titles = [a.getText() for a in soup.select('h3.lister-item-header a')]
            links = [a.attrs.get('href') for a in soup.select('h3.lister-item-header a')]
            df_dict = {'title': [], 'genre': [], 'description': [], 'img_link': []}

            for index in range(0, len(movies)):
                try:
                    temp = []

                    film_url = 'https://www.imdb.com'+links[index]
                    film_response = requests.get(film_url)
                    film_soup = BeautifulSoup(film_response.text, 'html.parser')

                    # Title
                    # title = str(list(soup.select('h1.sc-dae4a1bc-0'))[0])
                    # title = film_soup.body.find_all(text="Original")
                    # print(title)
                    # title = re.sub(r'</span>', '', title)
                    # title = re.sub(r'<.*>', '', title)
                    # print(titles[index])
                    # title = translator.translate(titles[index])

                    # Image
                    image_links = [img.attrs.get('src') for img in film_soup.select('img')]
                    image_url = image_links[0]
                    img = Image.open(requests.get(image_url, stream = True).raw)
                    a = i*10+index+1
                    if a<100:
                        img.save(f'Lab_2/images/{genre}_0{a}.jpg')
                        a = '0'+str(a)                        
                    else:
                        img.save(f'Lab_2/images/{genre}_{a}.jpg')

                    # Short description
                    description = str(list(film_soup.select('span.sc-16ede01-1'))[0])
                    description = re.sub(r'</span>', '', description)
                    description = re.sub(r'<.*>', '', description)

                    df_dict['title'].append(titles[index])
                    temp.append(titles[index])
                    df_dict['genre'].append(genre)
                    df_dict['description'].append(description)
                    temp.append(description)
                    df_dict['img_link'].append(f'{genre}_{a}.jpg')
                    temp.append(f'{genre}_{a}.jpg')
                    print(temp)

                    test=open('Lab_2/log.txt', 'a', encoding="utf-8")
                    test.write(temp[0]+";"+temp[1]+";"+temp[2]+'\n')
                    test.close()

                    time.sleep(random.randint(1, 10)/10)
                except:
                    print(f'\n{index} - error\n')
                    continue
        
            temp_df = pd.DataFrame(df_dict)
            df = df.append(temp_df, ignore_index=True)
            df.to_csv('Lab_2/data.csv', sep=';', index=None)
