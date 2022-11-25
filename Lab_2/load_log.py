# -*- coding: utf-8 -*-
import re
import pandas as pd

if __name__=="__main__":

    df = pd.read_csv('Lab_2/log.txt', sep=';', encoding='utf-8')
    genre = []
    for i in range(len(df)):
        genre.append(re.sub("[^A-Za-z]", "", re.sub(".jpg","",df['img_link'].iloc[i])))
    df['genre'] = genre
    df.to_csv('Lab_2/data.csv', sep=';', index=None)
    # print(df[0:2])