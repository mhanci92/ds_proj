from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np



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
recipeHash = {}

# a list of all (not unique) ingredients
zutaten = ''



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
				#print(zutaten_string)
			row_string += '{}'.format(zutaten_string)

			# adds the ingredients of the new recipe to the general list of ingredients
			global zutaten 
			zutaten += zutaten_string

			# transforms each recipe´s ingredients´ list into a set. we re going to use 
			# this as a value in recipeHash
			zutatenSet = set(zutaten_string)

			# add the rating after all ingredients
			row_string += '{}\n'.format(avg_rating)

			# add the recipe title and ingredient set to the recipeHash
			recipeHash={recipe_title:zutatenSet}


			#row_string += "\n"
			# Write each recipe, row by row, into the previously created text file
			recepts_file.write(row_string)
			reset_string(row_string)
			print(str(recipe_title.text.strip()) + " added to the text file!")

	recepts_file.close()
	# Close the driver			
	driver.quit()		


# list of all recipe names from the hashmap keys
#recipeNames = recipeHash.keys()




# create the numpy matrix filled with binary values for each recipe
def createNumpyMatrix():

	# this is the hashmap which is going to be filled with binary values for the recipes´ ingredients
	recipeBinary = {}

	# a set of unique ingredients
	ingredientsSet = set(zutaten)

	# transform the ingredients set in a list of unique ingredients to access it
	ingredientsList = list(ingredientsSet)


	# for each recipe in the hashmap
	for recipe in recipeHash:

		# a numpy array filled with 0s is created. it is as long as the list of unique ingredients
		numpyIngredients = np.zeros(len(ingredientsList), dtype=np.int)

		# go through the general ingredients set to check if the ingredient is contained into the recipe set
		for ingr in ingredientsList:
			# if the element in the general set is also in the ingredients set of the single recipe
			if ingr in recipeHash[recipe]:
				# then a 1 is added to the binary array of the single recipe at the ingredient´s index
				np.put(numpyIngredients,ingr,1)


		# the binary hashmap is updated with the new recipe and the corresponding binary array of ingredients
		recipeBinary['recipe']= numpyIngredients


	

	# it creates and populates the numpy matrix with the binary values
	numpy_matrix = np.matrix(recipeBinary.values())

	# tranforms the matrix into a string, so that it can be printed
	matrix_string = str(numpy_matrix)

	print("et voila!: \n" + matrix_string)








menueart_scraper()

createNumpyMatrix()

