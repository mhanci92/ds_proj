from selenium import webdriver
from bs4 import BeautifulSoup

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

# hashmap (dictionary) of recipe names (keys) and corresponding ingredient sets (values).
# it s going to be filled up in the menueart_scraper() function
recipeHash = collections.OrderedDict()

# a list with all (not unique) ingredients
zutaten = []



# TO-DO: Refactoring
def menueart_scraper():
	# Initialize the driver
	driver = initialize_driver()

	# Set the important Urls that are required later
	baseUrl = "http://www.chefkoch.de"
	receptsUrl = 'http://www.chefkoch.de/rezepte/'

	# Additional string to add to the end the the recipe url in order to make that the ingredients listed are for a two people meal
	two_meals = '?portionen=2'

	soup = BeautifulSoup(get_page_source(receptsUrl, driver), 'lxml')

	ul = soup.find('ul', id='recipe-tag-list')
	menuart_li = ul.findChildren('li', class_='recipe-tag-list-item')[2]
	menuart_links = menuart_li.find_all('a', class_='sg-pill')

	# Create the text file that will contain the information about every single recipe
	recepts_file = create_file("Rezepte")


	# Loop through the all the categories of Menueart
	for link in menuart_links:

		row_string = ''

		# Get the name of the menuart category that we will get recipes from
		category_name = link.text.strip()

		# Build the link for the category to scrape from
		url = build_menu_item_url(baseUrl, link)

		# Initialize a soup object based on the content from the link
		soup = BeautifulSoup(get_page_source(url, driver), 'lxml')

		# Now find the search list containing all the recipes of the previously selected menu item
		search_list = soup.find('ul', class_='search-list')

		# Find all the items that the previously found list contains
		search_list_items = search_list.find_all('li', class_='search-list-item')

		# Now loop through the list of items and scrape data from every single recipe
		for recipe in search_list_items:
			row_string += "{}\t".format(category_name)
			recipe_a_link = recipe.findChild('a')
			full_url_to_recipe = build_menu_item_url(baseUrl, recipe_a_link)

			# Get source code of the recipe 
			soup = BeautifulSoup(get_page_source(full_url_to_recipe+two_meals, driver), 'lxml')

			### Start scraping information from the current recipe ###

			# Get the title of the recipe
			recipe_title = soup.find('h1', class_='page-title')

			
			row_string += '{}\t'.format(recipe_title.text.strip())

			# get the average rating for each recipe
			rating = soup.find_all('span', class_='rating__average-rating')[0].text.strip()

			# leave out the average symbol at the beginning of the rating
			avg_rating = rating[1:]

			# Get the table which contains all the ingredients
			zutaten_table = soup.find('table', class_='incredients')

			zutaten_string = ''

			list1 = []

			# in this list there are all ingredients belonging to the same recipe
			inTheRecipe = []

			# Go through every single row of the table containing the ingredients
			for row in zutaten_table.find_all('tr'):
				# Get the required amount of each ingredient that is needed for a recipe
				#amount = row.find('td', class_='amount').text.strip()
				# Get the name of each ingredient that is needed for a recipe
				ingredient = row.find_all('td')[1].text.strip()
				# check if the ingredient string is made up of more than the ingredient itself
				if ',' in ingredient:
					# split the string at the comma
					list1 = ingredient.split(',')
					#print('first element: '+ list1[0])
					# get the first substring which contains the ingredient
					ingredient = list1[0]
					# empty the list to make space for the next 
					del list1[:]
				#print('the ingredient '+ ingredient)
				zutaten_string += '{}\t'.format(ingredient)

				# each ingredient is saved into the recipe´s list
				inTheRecipe = zutaten_string.split('\t')
				
			# adds the ingredients of the new recipe to the general list of ingredients
			global zutaten
			zutaten.extend(inTheRecipe)

			row_string += '{}'.format(zutaten_string)

		

			# transforms each recipe´s ingredients´ list into a set. we re going to use 
			# this as a value in recipeHash
			#recipeSet = set(inTheRecipe)

			# add the rating after all ingredients
			row_string += '{}\n'.format(avg_rating)

			# add the recipe title and ingredients list to the recipeHash
			recipeHash[recipe_title.text.strip()] = inTheRecipe


			#row_string += "\n"
			# Write each recipe, row by row, into the previously created text file
			recepts_file.write(row_string)
			reset_string(row_string)
			print(str(recipe_title.text.strip()) + " added to the text file!")

	recepts_file.close()
	# Close the driver			
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
    print(recipe_hash)
    return recipe_hash

# it creates an ordered list of ratings (same order as recipes). these are categorized according to rating classes, 
# so if a rating is between 2 and 3, it belongs to class 3 and so on. this is returned as a pandas dataframe and saved to a csv.
def create_ratings_list(text_file):
	with open(text_file, 'r') as tFile:
		reader = csv.reader(tFile, dialect ='excel-tab')
		ratings_hash = collections.OrderedDict()
		for line in reader:

			# extract the rating and categorize it
			rating = float(line[len(line)-1].strip().replace(',','.'))
			if rating >= 0 and rating < 1 :
				rating = 1
			elif rating >= 1 and rating < 2 :
				rating = 2
			elif rating >= 2 and rating < 3 :
				rating = 3
			elif rating >= 3 and rating < 4 :
				rating = 4
			elif rating >= 4 and rating < 5 :
				rating = 5

			# extend the hashmap with recipe names and corresponding ratings
			if line[1] in ratings_hash:
				ratings_hash[line[1] + str(len(ratings_hash))] = rating
			else:
				ratings_hash[line[1]] = rating

	ratingsDF = pd.DataFrame.from_dict(data=ratings_hash,orient='index')
	ratingsDF.to_csv('ratingsDF.csv', sep=',', header = ratings_hash.keys(), encoding = 'utf-8')
	return ratingsDF



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







	# # creates a matrix full of 0s. the nr of rows corresponds to the nr of recipes and the nr of columns to the nr of total ingredients
	# rezepten_matrix = np.zeros((len(recipeHash.keys()),len(ingredientsList)),dtype=np.int)

	# for recipe_idx,recipe_ingr in enumerate(recipeHash.values()):

	# 	for zutat_idx, ingr in enumerate(ingredientsList):

	# 		if ingr in recipe_ingr:

	# 			rezepten_matrix[recipe_idx,zutat_idx] = 1


	
	# # tranforms the matrix into a string, so that it can be printed
	# matrix_string = str(rezepten_matrix)

	# print("et voila!: \n" + matrix_string)

	# np.savetxt("recipeMatrix.csv", rezepten_matrix, fmt='%i',delimiter=',')


	# return rezepten_matrix










#menueart_scraper()
#print(len(create_uniqueIngredients_list('Rezepte.txt')))
#print(str(create_recipeIngredients_list(create_uniqueIngredients_list('Rezepte.txt'))))
#create_recipe_hash('Rezepte.txt')
#menueart_scraper()
#createBinaryDF()

create_ratings_list('Rezepte.txt')



