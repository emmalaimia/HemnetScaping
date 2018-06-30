
"""This script scrapes the listings on the Hemnet Slutpris section for Stockholm and outputs a csv with a table with the following variables:
adress, stadsdel, maklare, storlek, rum, avgift, datum, slutpris, pris_per_meter, percent_over, utgangs_pris"""

import pandas as pd
import requests
import bs4 as bs
import pandas as pd
import re as re

url = 'https://www.hemnet.se/salda/bostader?location_ids%5B%5D=473379&sold_age=6m'
response = requests.get(url)
code = response.text
parsed = bs.BeautifulSoup(code, "html.parser")
listings = parsed.findAll('div',{'class':'sold-property-listing'})

#Find address
def get_address(listings):
    addresser = []
    for entry in listings:
        locations = entry.findAll('div', {'class':'sold-property-listing__location'})
        for entry in locations:
            str_entry = str(entry)
            id_location = str_entry.find('item-link')
            if id_location>=0:
                start_location = id_location + 11
                remaining = str_entry[start_location:]
                end_location = remaining.find('<')
                remaining = remaining[:end_location]
            else:
                remaining = 'Saknas'
            addresser.append(remaining)
        return addresser

#Find neighborhood
def get_stadsdel(listings):
    stadsdelar = []
    for entry in listings:
        locations = entry.findAll('div', {'class':'sold-property-listing__location'})
        for entry in locations:
            str_entry = str(entry)
            id_location = str_entry.find('<span class="item-link"') + 1
            if id_location>0:
                start_location = id_location + 25
                remaining = str_entry[start_location:]
                remaining = remaining.lstrip(' ')
                end_location = str(remaining).find(',')
                remaining = remaining[:end_location]
            else:
                remaining = 'Saknas'
            stadsdelar.append(remaining)
        return stadsdelar

#Find broker
def get_maklare(listings):
    brokers_list = []
    for entry in listings:
        brokers = entry.findAll('div', {'class':'sold-property-listing__broker'})
        for entry in brokers:
            str_entry = str(entry)
            id_location = str_entry.find('sold_clicks')
            if id_location>0:
                remaining = str_entry[id_location:]
                start_location = remaining.find('>') + 1
                end_location = remaining.find('<')
                remaining = remaining[start_location:end_location]
            else:
                remaining = 'Saknas'
            brokers_list.append(remaining)
    return brokers_list 
      
#Find final price
def get_slutpris(listings):
    prices_extracted = []
    #Extract section of HTML that contains price information
    for entry in listings:
        subentry = entry.findAll('div',{'class':'sold-property-listing__price'})
        for sub in subentry:
            sub2 = sub.findAll('div', {'class': 'clear-children'})
            for sub3 in sub2:
                price = sub3.findAll('span', {'class': 'sold-property-listing__subheading sold-property-listing--left'})
                if len(price)>0:
                    prices_extracted.append(price)
    #Remove evertying in this part before Slutpris
    prices_to_clean = [str(price)[str(price).find('Slut'):] 
                        for price 
                        in prices_extracted]
    #Only keep the numeric part of the string
    clean_prices = [int(''.join(c for c in i if c.isdigit())) 
                    for i 
                    in prices_to_clean]
    return clean_prices
    
print(get_address(listings))
#print(get_stadsdel(listings))
#print(get_maklare(listings))
#print(get_slutpris(listings))

#print(pd.DataFrame(
#    {'Adress': get_address(listings),
#     'Stadsdel': get_stadsdel(listings),
#     'Maklare': get_maklare(listings),
#     'Slutpris': get_slutpris(listings)
#    }))





  