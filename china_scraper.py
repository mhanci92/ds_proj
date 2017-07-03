from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import collections
np.set_printoptions(threshold=np.inf)

class ChefkochScraper(object):

	def __init__(self):
		self.next_links = []
		# a list with all (not unique) ingredients		
		self.zutaten = []
		# hashmap (dictionary) of recipe names (keys) and corresponding ingredient sets (values).
		# it s going to be filled up in the menueart_scraper() function
		self.recipeHash = collections.OrderedDict()
		self.baseUrl = "http://www.chefkoch.de"
		self.receptsUrl = "http://www.chefkoch.de/rezepte/"		


	def get_page_source(self, link_of_page, driver):
		driver.get(link_of_page)
		return driver.page_source

	def initialize_driver(self):
		#driver = webdriver.PhantomJS(executable_path=r'C:\Users\AnNa\Desktop\phantomjs')
		driver = webdriver.PhantomJS(executable_path=r'/Users/martinhanci/Documents/Web-Scraping/phantomjs-2.1.1-macosx/bin/phantomjs')
		return driver	

	# Simple Method that is supposed to combine the baseUrl with a href suffix of the second parameter
	def build_link(self, baseUrl, link_to_get_href_from):
		href = link_to_get_href_from['href']
		return self.baseUrl + href	

	def create_file(self, file_name):
		return open(file_name + ".txt", "w")

	def reset_string(self, string_to_reset):
		string_to_reset = ''	

	def menueart_scraper(self):
		driver = self.initialize_driver()

		two_meals = '?portionen=2'

		soup = BeautifulSoup(self.get_page_source(self.receptsUrl, driver), 'lxml')


		try:
			ul = soup.find('ul', id='recipe-tag-list')
			menuart_li = ul.findChildren('li', class_='recipe-tag-list-item')[6]
			menuart_links = menuart_li.find_all('a', class_='sg-pill')
		except AttributeError as ae:
			print("Crucial website info is missing!")
			print(ae)
			raise
		except IndexError as ie:
			print("Crucial website info is missing!")
			print(ie)
			raise 		

		recepts_file = self.create_file("Rezepte")

		temp_value = 0
		# Loop through the all the categories of Menueart
		for link in menuart_links:

			row_string = ''

			# Get the name of the menuart category that we will get recipes from
			cuisine = link.text.strip()

			# If cuisine is equal to one of these, skip it and continue with the next cuisine in the list 
			if cuisine != "China":
				continue

			# Build the link for the category to scrape from
			url = self.build_link(self.baseUrl, link)

			# Initialize a soup object based on the content from the link
			soup = BeautifulSoup(self.get_page_source(url, driver), 'lxml')

			a_sort_acc_date = soup.find('a', class_='searchresult-sorting-by-date')
			sort_Acc_To_Date_Full_Link = self.build_link(self.baseUrl, a_sort_acc_date)

			soup = BeautifulSoup(self.get_page_source(sort_Acc_To_Date_Full_Link, driver), 'lxml')

			# Now find the search list containing all the recipes of the previously selected menu item
			search_list = soup.find('ul', class_='search-list')

			if search_list != None:
				# Find all the items that the previously found list contains
				search_list_items = search_list.find_all('li', class_='search-list-item')			
			else:
				continue

			weiter_a_link = soup.select('a.ck-pagination__link.ck-pagination__link-prevnext.ck-pagination__link-prevnext--next.qa-pagination-next')
			self.next_links.append(weiter_a_link)
			loop_counter = 0

			while self.next_links[0] != None:
				if loop_counter > 0:	
					weiter = self.build_link(self.baseUrl, weiter_a_link[0])
					soup2 = BeautifulSoup(self.get_page_source(weiter, driver), 'lxml')
					search_list_items = soup2.find_all('li', class_='search-list-item')
					weiter_a_link = soup2.select('a.ck-pagination__link.ck-pagination__link-prevnext.ck-pagination__link-prevnext--next.qa-pagination-next')
					self.next_links[0] = weiter_a_link
				loop_counter += 1								

				# Now loop through the list of items and scrape data from every single recipe
				for idx, recipe in enumerate(search_list_items):

					recipe_a_link = recipe.findChild('a')

					if recipe_a_link != None:
						full_url_to_recipe = self.build_link(self.baseUrl, recipe_a_link)
					else:
						row_string = "{}".format("\n")
						continue	

					soup2 = BeautifulSoup(self.get_page_source(full_url_to_recipe+two_meals, driver), 'lxml')

					### Start scraping information from the current recipe ###

					# Get the title of the recipe
					recipe_title = soup2.find('h1', class_='page-title')

					if recipe_title != None:
						row_string += "{}\t".format(recipe_title.text.strip())
						row_string += "{}\t".format(cuisine)
					else:
						print("Couldn't find recipe title: " + recipe_title)
						print("Skipping row..")
						row_string = "{}".format("\n")
						continue		

					# get the average rating for each recipe
					avg_rating = ''			
					try:
						rating = soup2.find('span', class_='rating__average-rating').text.strip()
						# leave out the average symbol at the beginning of the rating				
						avg_rating = rating[1:]
					except AttributeError:	
						avg_rating = "0"


					# Get the table which contains all the ingredients
					zutaten_table = soup2.find('table', class_='incredients')

					if not zutaten_table:
						print("zutaten_table is empty!")
						continue

					if zutaten_table == None:
						print("zutataten_table is could not be found or is not existing!")
						continue

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
						zutaten_string += "{}\t".format(ingredient)

						# each ingredient is saved into the recipe´s list
						inTheRecipe = zutaten_string.split("\t")
						
					# adds the ingredients of the new recipe to the general list of ingredients
					self.zutaten
					self.zutaten.extend(inTheRecipe)

					row_string += "{}".format(zutaten_string)

					# transforms each recipe´s ingredients´ list into a set. we re going to use 
					# this as a value in recipeHash
					#recipeSet = set(inTheRecipe)

					# add the rating after all ingredients
					row_string += "{}\n".format(avg_rating)


					#row_string += "\n"
					# Write each recipe, row by row, into the previously created text file
					recepts_file.write(row_string)
					self.reset_string(row_string)
					print(str(recipe_title.text.strip()) + " added to the text file!")

			recepts_file.close()
			driver.quit()		


scraper = ChefkochScraper()
scraper.menueart_scraper()
