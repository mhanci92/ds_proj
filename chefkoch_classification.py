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


recipeMatrix = pd.read_csv('recipeMatrix.csv', encoding = 'utf-8')
ratingsDF = pd.read_csv('ratingsDF.csv', encoding = 'utf-8')



# it reduces the dimensionality of both datasets and returns them
def reduce_datasets():
	
	# creates a numpy array with recipes out of the dataframe 
	recipes_dataset = reduce_dimensionality(recipeMatrix)
	# creates a numpy array with ratings out of the dataframe
	ratings_dataset = reduce_dimensionality(ratingsDF)
	return recipes_dataset,ratings_dataset


# it uses pca for dimensionality reduction
def reduce_dimensionality(dataset):

	pca = PCA()
	ds = pca.fit_transform(dataset)
	return ds

# it splits the dataset into train, validation and test sets and returns their arrays
def split_ds(dataset):

	train, val, test = np.split(dataset.sample(frac=1), [int(.6*len(dataset)), int(.8*len(dataset))])
	return train.as_matrix(), val.as_matrix(), test.as_matrix()


# it returns arrays for each of the recipe training, validation and test sets
def split_recipeDS():

	recipes = reduce_datasets()[0]
	x_train, x_validate, x_test = split_ds(recipes)
	return x_train, x_validate, x_test



# it returns arrays for each of the ratings training, validation and test sets
def split_ratingsDS():

	ratings= reduce_datasets()[1]
	y_train, y_validate, y_test = split_ds(ratings)
	return y_train, y_validate, y_test



# it creates and returns the svc model
def create_svc():

	svc = svm.SVC(gamma=0.001, C=100., kernel='linear')







