from selenium import webdriver
from bs4 import BeautifulSoup


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
				if ',' in ingredient:
					list1.append(ingredient.split(','))
					ingredient = list1[0]
					del list1[:]
				zutaten_string += '{}\t, '.format(ingredient)
			row_string += '{}\n'.format(zutaten_string)	
			#row_string += "\n"
			# Write each recipe, row by row, into the previously created text file
			recepts_file.write(row_string)
			reset_string(row_string)
			print(str(recipe_title.text.strip()) + " added to the text file!")

	recepts_file.close()
	# Close the driver			
	driver.quit()		



menueart_scraper()	
