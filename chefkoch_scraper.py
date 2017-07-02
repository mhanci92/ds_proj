from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from random import randint, shuffle

import numpy as np
import collections
import pandas as pd
import csv
np.set_printoptions(threshold=np.inf)



# Simple method that returns the page source of the link that is passed as a parameter
def get_page_source(link_of_page, driver):
	driver.get(link_of_page)
	return driver.page_source

# Method that initializes a driver and returns it
def initialize_driver():
	driver = webdriver.PhantomJS(executable_path=r'C:\Users\AnNa\Desktop\phantomjs')
	return driver	

# Simple Method that is supposed to combine the baseUrl with a href suffix of the second parameter
def build_menu_item_url(baseUrl, link_to_get_href_from):
	href = link_to_get_href_from['href']
	return baseUrl + href	

# Method that creates a text file by the name that is passed as the parameter
def create_file(file_name):
	return open(file_name + ".txt", "w")


def reset_string(string_to_reset):
	string_to_reset = ''	



def menueart_scraper():

	driver = initialize_driver()

	baseUrl = "http://www.chefkoch.de"
	receptsUrl = 'http://www.chefkoch.de/rezepte/'

	soup = BeautifulSoup(get_page_source(receptsUrl, driver), 'lxml')

	ul = soup.find('ul', id='recipe-tag-list')
	menuart_li = ul.findChildren('li', class_='recipe-tag-list-item')[2]
	menuart_links = menuart_li.find_all('a', class_='sg-pill')

	recepts_file = create_file("Rezepte")

	for link in menuart_links:

		row_string = ''
		category_name = link.text.strip()
		url = build_menu_item_url(baseUrl, link)
		soup = BeautifulSoup(get_page_source(url, driver), 'lxml')
		search_list = soup.find('ul', class_='search-list')
		search_list_items = search_list.find_all('li', class_='search-list-item')
        
		for recipe in search_list_items:
			row_string += "{}\t".format(category_name)
			recipe_a_link = recipe.findChild('a')
			full_url_to_recipe = build_menu_item_url(baseUrl, recipe_a_link)
			soup = BeautifulSoup(get_page_source(full_url_to_recipe, driver), 'lxml')
			recipe_title = soup.find('h1', class_='page-title')
			row_string += '{}\t'.format(recipe_title.text.strip())
			rating = soup.find_all('span', class_='rating__average-rating')[0].text.strip()
			avg_rating = rating[1:]
			zutaten_table = soup.find('table', class_='incredients')
			zutaten_string = ''
			list1 = []
            
			for row in zutaten_table.find_all('tr'):
				ingredient = row.find_all('td')[1].text.strip()
                
				if ',' in ingredient:
					list1 = ingredient.split(',')
					ingredient = list1[0]
					del list1[:]
				zutaten_string += '{}\t'.format(ingredient)
				
			row_string += '{}'.format(zutaten_string)
			row_string += '{}\n'.format(avg_rating)

			recepts_file.write(row_string)
			reset_string(row_string)
			print(str(recipe_title.text.strip()) + " added to the text file!")
			sleep_for = randint(3,10)
			sleep(sleep_for)


	recepts_file.close()			
	driver.quit()		

			

# this creates a list of all unique ingredients from the txt file
def create_uniqueIngredients_list(text_file):
    with open(text_file, 'r') as tFile:
        reader = csv.reader(tFile, dialect = 'excel-tab')
        recipe_ingredients = []
        for line in reader:
        	recipe_ingredients.extend(create_recipeIngredients_list(line))
    unique_ingredients = list(set(recipe_ingredients))
    #print(str(unique_ingredients))
    return unique_ingredients


# hilfsmethode. it creates a list of all ingredients for one single recipe
def create_recipeIngredients_list(row):
    row = list(filter(None, row))
    ingredients = []
    for index, element in enumerate(row):
        if index > 1 and index < len(row)-1:
            ingredients.append(element)

    return ingredients


# it creates a hashmap (ordered dictionary) of all recipe names (keys) and corresponding ingredients list (values)
# out of the txt file
def create_recipe_hash(text_file):
    with open(text_file, 'r') as tFile:
        reader = csv.reader(tFile, dialect='excel-tab')
        recipe_hash = collections.OrderedDict()
        for line in reader:
        	if line[1] in recipe_hash:
        		recipe_hash[line[1] + str(len(recipe_hash))] = create_recipeIngredients_list(line)
        	else:
        		recipe_hash[line[1]] = create_recipeIngredients_list(line)
    #print(recipe_hash)
    return recipe_hash

# it creates an ordered list of ratings (same order as recipes). these are categorized according to rating classes, 
# so if a rating is between 2 and 3, it belongs to class 3 and so on. this is returned as a pandas dataframe and saved to a csv.
def create_ratings_list(text_file):
	with open(text_file, 'r') as tFile:
		reader = csv.reader(tFile, dialect ='excel-tab')
		ratings = []
		for line in reader:

			# extract the rating and categorize it
			rating = float(line[len(line)-1].strip().replace(',','.'))
			ratings.append(np.ceil(rating))

	ratingsNP = np.array(ratings)
	ratingsNP = pd.DataFrame(ratingsNP)
	# np.savetxt('ratingsNP.csv', ratingsNP, delimiter = ',')
	# print(ratingsNP.size)
	ratingsNP.to_csv('ratingsNP.csv', sep = ',', encoding = 'utf-8')
	
	return ratingsNP
	## return ratings_hash.values()



# assign binaries to each recipe and create and return a pandas dataframe out of them
def createBinaryDF():

	# this is the hashmap which is going to be filled with binary values for the recipes´ ingredients
	recipeBinary = collections.OrderedDict()
	recipe_hash = create_recipe_hash('Rezepte.txt')
	ingredientsList = create_uniqueIngredients_list('Rezepte.txt')
	for rec_nr, rec_i in enumerate(recipe_hash):
		recipeBinary[list(recipe_hash)[rec_nr]] = []

	# fill the hashmap with recipe names as keys and binary values for the corresponding ingredients
	for recipe_idx,recipe_ingr in enumerate(recipe_hash.values()):
		for zutat_idx, ingr in enumerate(ingredientsList):
			if ingr in recipe_ingr:
				recipeBinary[list(recipe_hash)[recipe_idx]].append(1)
			else:
				recipeBinary[list(recipe_hash)[recipe_idx]].append(0)

	# create a pandas dataframe object out of the recipes´ hashmap
	recipeDF = pd.DataFrame.from_dict(recipeBinary,orient='index')

	# save the dataframe into a csv 
	recipeDF.to_csv('recipeMatrix.csv', sep = ',', header = ingredientsList, encoding= 'utf-8')

	return recipeDF


#menueart_scraper()
#print(len(create_uniqueIngredients_list('Rezepte.txt')))
#print(str(create_recipeIngredients_list(create_uniqueIngredients_list('Rezepte.txt'))))
#create_recipe_hash('Rezepte.txt')
createBinaryDF()
create_ratings_list('Rezepte.txt')



