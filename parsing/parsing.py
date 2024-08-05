import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging
from tqdm import tqdm
import time


print('#########___START PARSING SCRIPT ___#########')
current_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", current_time)
print()
print(f"___ Current date and time ___  << {formatted_time} >>")
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")



def get_urls():
    print('\n#######################################################\n')
    print('___ LOAD URLS ___')

    sub_url = []
    for page in tqdm(range(1, int(input('How many pages do you want? ')) + 1)):
        url = f'https://www.mashina.kg/search/all/?page={page}'
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            objects = soup.find("div", class_="search-results-table")
            lincs = objects.find_all('div', class_="list-item list-label")
            for ur in lincs:
                sub_url.append(ur.find('a')['href'])
        except Exception:
            logging.error(f'Error fetching URL {url}')
            continue

    print(f'\n ___ Received {len(sub_url)} URLS ___')
    logging.info(f'\n ___ Received {len(sub_url)} URLS ___')

    urls = ["https://www.mashina.kg" + i for i in sub_url]

    return urls

def save_urls(urls: list):
    urls_df = pd.DataFrame(urls, columns=['URL'])
    urls_df.to_csv('urls.csv', index=False)
    print('URLs saved to urls.csv')
    logging.info('URLs saved to urls.csv')

def parsing_single_url(ur):
    response = requests.get(ur)
    soup = BeautifulSoup(response.text, "html.parser")
    objects = soup.find('div', class_='tab-pane fade in active')
    atr_dict = {}

    try:
        atributs = objects.find_all('div', class_='field-row clr')
        for atr in atributs:
            key = atr.find('div', class_='field-label').text.strip().replace('\n', '')
            val = atr.find('div', class_='field-value').text.strip().replace('\n', '')
            atr_dict[key] = val
    except Exception:
        logging.error(f'Error in parsing atributs for {ur}')

    try:
        views = soup.find('span', class_='listing-icons views').text
        atr_dict['views'] = views
    except Exception:
        logging.error(f'Error in parsing views for {ur}')

    try:
        hearts = soup.find('span', class_='listing-icons heart').text
        atr_dict['hearts'] = hearts
    except Exception:
        logging.error(f'Error in parsing hearts for {ur}')

    try:
        tel_number = soup.find('div', class_='number').text
        atr_dict['tel_number'] = tel_number
    except Exception:
        logging.error(f'Error in parsing tel_number for {ur}')

    try:
        USD_price = soup.find('div', class_='price-dollar').text.replace('$ ', '').replace(' ', '')
        KGS_price = soup.find('div', class_='price-som').text.replace(' сом', '').replace(' ', '')
        brend = soup.find('div', class_='head-left').find('h1').text
        publicated = soup.find('div', class_='subblock upped-at').text.strip()
        atr_dict['USD_price'] = USD_price
        atr_dict['KGS_price'] = KGS_price
        atr_dict['brend'] = brend
        atr_dict['publicated'] = publicated
    except Exception:
        logging.error(f'Error in parsing USD_price,KGS_price,brend,publicated for {ur}')

    try:
        look_like_key = soup.find_all('div', class_='name')
        look_like_val = soup.find_all('div', class_='value')
        for i, j in zip(look_like_key, look_like_val):
            atr_dict[i.text] = j.text
    except Exception:
        look_like = None

    return atr_dict

urls_ = get_urls()
save_urls(urls_)

urls = pd.read_csv('urls.csv')
urls = urls['URL'].tolist()
print('######  PARSING ######')
output_file = f'mashina_kg_{formatted_time}.csv'
all_cars = []
size_of_chunk = 50
for i in tqdm(range(0, len(urls), size_of_chunk)):
    chunk = urls[i:i + size_of_chunk]
    cars = []
    for ur in tqdm(chunk):
        try:
            car_data = parsing_single_url(ur)
            cars.append(car_data)
        except Exception as e:
            logging.error(f"Error parsing URL {ur}")

    if cars:
        df_cars = pd.DataFrame(cars)
        all_cars.extend(cars)
        if not os.path.isfile(output_file):
            df_cars.to_csv(output_file, index=False)
        else:
            df_cars.to_csv(output_file, mode='a', header=False, index=False)
        logging.info(f'___ Data for chunk {i // size_of_chunk + 1} appended to {output_file} ___')



df = pd.DataFrame(all_cars)

print('___ DATA INFO ___\n')
print(df.info())
print(f'\n\nNumber of unique phone numbers: {df.tel_number.unique().shape[0]} / {df.shape[0]}\n')

df.to_csv(output_file, index=False)
print(f'___ File << {output_file} >> saved ___')
print('##### END #####')