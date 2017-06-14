# -*- coding: utf-8 -*-
"""
Created on Sun May 21 14:43:17 2017

@author: AnNa
"""

from bs4 import BeautifulSoup
import urllib

# address the page you need 
reweFood = "https://shop.rewe.de/c/nahrungsmittel/"

# open the page you need
page = urllib.request.urlopen(reweFood)

# transform the page into a beautifulsoup object in order to parse its elements
soup = BeautifulSoup(page,"lxml")

# file with the names, prices and quantities for each product
file = open('reweScraper.txt', 'w')

namesList = []
pricesList = []

# find all the content bodies with the products´ information
#products = soup.findAll('a',class_="rs-productlink rs-qa-product-details-link rs-js-key-navigation rs-producttile__title")

# get all product names
'''
for item in products:    
    namesList.append(item.getText())
    

# find all product prices
prices = soup.findAll('mark',class_='rs-price rs-price--fancy rs-qa-price')
for price in prices:
    predecimal = price.find('span', class_='rs-price__predecimal').getText()
    decimal = price.find('span', class_= 'rs-price__decimal').getText()
    number = str(predecimal)+','+str(decimal)
    pricesList.append(number)


#for x,y in namesList,pricesList:
#    file.write(x + ',' + y + '\n')

#for x in pricesList:
#    file.write(x + '\n')
'''
products = soup.findAll('div',class_='rs-tile rs-tile--product rs-js-product-item')

for item in products:
    box = item.findAll('div', class_='rs-media__body')
    for info in box:
        name = info.findAll('a',class_="rs-productlink rs-qa-product-details-link rs-js-key-navigation rs-producttile__title")
        for n in name:
            namesList.append(n.getText())
        price = info.findAll('mark',class_='rs-price rs-price--fancy rs-qa-price')
        for p in price:
            predecimal = p.find('span', class_='rs-price__predecimal').getText()
            decimal = p.find('span', class_= 'rs-price__decimal').getText()
            number = str(predecimal)+','+str(decimal)
            pricesList.append(number)

for x in pricesList:
    file.write(x + '\n')
            
    
file.close()







