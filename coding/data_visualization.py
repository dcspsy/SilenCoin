# -*- coding: utf-8 -*- #
import pandas as pd
import numpy as np
import pycountry
import os
# read data
read_cities = pd.read_csv('./data/worldcitiespop.txt', sep=",", usecols=['Country', 'City', 'Latitude', 'Longitude'])
read_coins = pd.read_json('./data/chain.json')

cities = pd.pivot_table(read_cities,index=['City'], aggfunc='mean')
coins = read_coins.chain.values
coins_hash = np.array([i['previous_hash'] for i in coins])

cities_index = np.arange(cities.shape[0])
first_city = np.where(cities.index.values == 'beijing')[0][0]
cities_list = [first_city]


for i in coins_hash:
    seed = sum([ord(j) for j in i])
    np.random.seed(seed)
    city_index = np.random.choice(cities_index, 1)[0]
    cities_index = cities_index[cities_index !=city_index]
    cities_list.append(city_index)

world = pd.DataFrame(cities.iloc[cities_list])
world['order'] = np.arange(coins_hash.shape[0]+1)
countries = read_cities.iloc[cities_list, 0].apply(lambda x: pycountry.countries.get(alpha_2=x.upper()).name)
countries = countries.drop_duplicates()

world.to_csv('./output/world.csv')
countries.to_csv('./output/countries.csv', index=False)


def images_html_code():
    file_name = './output/images_html_code.txt'
    images_path = './images/'
    images = sorted([i for i in os.listdir(images_path) if i.split('.')[1]=='jpg'])

    with open(file_name, 'w') as f:
        f.write('<div class="container">')
        for image in images:
            image_path = images_path +image
            s = '\t<div class="imgShow"><a href="{}"><img src="{}"/></a> </div>\n'.format(image_path, image_path)
            f.write(s)
        f.write('</div>')


images_html_code()

