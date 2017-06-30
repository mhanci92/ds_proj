# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:27:15 2017

@author: AnNa
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn import svm
from sklearn.cross_validation import train_test_split



def read_datasets():
	
	# creates a numpy array with recipes out of the dataframe 
	recipes_dataset = reduce_dimensionality(pd.read_csv('recipeMatrix.csv', encoding = 'utf-8'))
	# creates a numpy array with ratings out of the dataframe
	ratings_dataset = reduce_dimensionality(pd.read_csv('ratingsDF.csv', encoding = 'utf-8'))
	return recipes_dataset,ratings_dataset



def reduce_dimensionality(dataset):

	pca = PCA()
	ds = pca.fit_transform(dataset)
	return ds


def split_ds(dataset):

	train, val, test = np.split(dataset.sample(frac=1), [int(.6*len(dataset)), int(.8*len(dataset))])
	return train, val, test





def split_recipeDS():

	recipes_dataset = read_datasets()[0]
	x_train, x_validate, x_test = split_ds(recipes_dataset)
	return x_train, x_validate, x_test




def split_ratingsDS():

	ratings_dataset = read_datasets()[1]
	y_train, y_validate, y_test = split_ds(ratings_dataset)
	return y_train, y_validate, y_test




def recipesDS_toArray():

	# it creates numpy arrays for the x data (recipes)
	training_recipes, validation_recipes, test_recipes = x_train.as_matrix(), x_validate.as_matrix(), x_test.as_matrix() 
	return training_recipes, validation_recipes, test_recipes




def ratingsDS_toArray():

	# it creates numpy arrays for the y data (ratings)
	training_ratings, validation_ratings, test_ratings = y_train.as_matrix(), y_validate.as_matrix(), y_test.as_matrix()
	return training_ratings, validation_ratings, test_ratings


# not yet refactored



# class labels = chefkoch sterne
cat = [1,2,3,4,5]

# this returns a shape
classifier = svm.LinearSVC(decision_function_shape='ovr')

# Fit the SVM model according to the given training data.
classifier.fit(train, cat)





