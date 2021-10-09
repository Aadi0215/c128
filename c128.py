from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('./chromedriver')
browser.get(start_url)
time.sleep(10)
headers = ['name', 'light_years_from_earth', 'second', 'planet_mars', 'third', 'stellar_magnitude', 'discovery_date', 'hyperlink', 'planet_type', 'planet_radius', 'oribital_radius', 'orbital_period', 'eccentricity']
planet_data = [] 
new_planet_list = []

def scrap():
    for i in range(0,10):
    
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for ul_tag in soup.find_all('ul', attrs = {'class', 'exoplanet'}):
            li_tags = ul_tag.find_all('li')

            temp_list = []
            for index, li_tags in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tags.find_all('a')[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tags.content[0])
                    except:
                        temp_list.append('')
            hyperlink_li_tag = li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov'+hyperlink_li_tag.find_all('a', href = True)[0]['href'])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id=primary_column]/footer/div/div/div/anv/span[2]/a').click()
        print(f'{i} page done 1')
    # with open('scrapper_2.csv', 'w') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow(headers)
    #     csv_writer.writerow(planet_data)
def scrapeMoreData(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        for tr_tag in soup.find_all('tr', attrs={'class':'fact_row'}):
            td_tags = tr_tag.find_all('td')
            temp_list = []
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all('div', attrs = {'class':'value'})[0].contents[0])
                except:
                    temp_list.append('')
            new_planet_list.append(temp_list)
    except:
        time.sleep(1)
        scrapeMoreData(hyperlink)
scrap()
for index, data in enumerate(planet_data):
    scrapeMoreData(data[5])
    print('page done 2', index+1)


final_planet_data_list = []

# for index, data in enumerate(planet_data):
#     final_planet_data_list.append(data + final_planet_data_list[index])

for index, data in enumerate(planet_data): 
    new_planet_list_element = new_planet_list[index] 
    new_planet_list_element = [elem.replace("\n", "") for elem in new_planet_list_element] 
    new_planet_list_element = new_planet_list_element[:7] 
    final_planet_data_list.append(data + new_planet_list_element)

with open('final.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerow('Final Planet Data')