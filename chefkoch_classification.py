# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:27:15 2017

@author: AnNa
"""
#import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd

#from sklearn.decomposition import PCA
#from sklearn.preprocessing import scale
from sklearn import svm
from sklearn import metrics
#from sklearn.manifold import Isomap
from sklearn.model_selection import train_test_split


recipeMatrix = pd.read_csv('recipeMatrix.csv', encoding = 'utf-8')
ratingsDF = pd.read_csv('ratingsDF.csv', encoding = 'utf-8').as_matrix()



# it reduces the dimensionality of both datasets and returns them (as numpy arrays) 
#def reduce_datasets():
#	
#	
#	recipes_dataset = reduce_dimensionality(recipeMatrix.shape)	
#	ratings_dataset = reduce_dimensionality(ratingsDF.shape)
#	return recipes_dataset,ratings_dataset


# it uses pca for dimensionality reduction
#def reduce_dimensionality(dataset):

#	pca = PCA()
#	ds = pca.fit_transform(dataset)
#	return ds

# it splits the dataset into train, validation and test sets and returns their arrays
def split_ds():

	x_train, x_te, y_train, y_te = train_test_split(recipeMatrix, ratingsDF, test_size = 0.40, random_state = 42)
	x_val, x_test, y_val, y_test = train_test_split(x_te,y_te, test_size = 0.20, random_state = 42)

	#train, val, test = np.split(dataset.sample(frac=1), [int(.6*len(dataset)), int(.8*len(dataset))])
	return x_train, x_val, x_test, y_train, y_val, y_test


# it returns arrays for each of the recipe training, validation and test sets
#def split_recipeDS():

#	recipes = reduce_datasets()[0]
#	x_train, x_validate, x_test = split_ds(recipes)
#	return x_train, x_validate, x_test



# it returns arrays for each of the ratings training, validation and test sets
#def split_ratingsDS():

#	ratings= reduce_datasets()[1]
#	y_train, y_validate, y_test = split_ds(ratings)
#	return y_train, y_validate, y_test


# it creates and fits the given svc model (linear, rbf, poly, sigmoid kernels...). it also returns the score 
def apply_svc(ker):

	x_train, x_validate, y_train, y_validate = split_ds()[0], split_ds()[1], split_ds()[3], split_ds()[4]	

	svc = svm.SVC(kernel = ker, decision_function_shape='ovr').fit(x_train.shape, y_train.shape)
	print(svc.score(x_validate, y_validate))
	return svc



# predicts results of the given svc
def predict_svc(ker):

	x_validate, y_validate = split_ds()[1], split_ds()[4]
	prediction = apply_svc(kernel = ker).predict(x_validate)

	print(prediction)
	print(y_validate)

	return prediction


# prints the classification report of the y-validation set and the prediction. this way you can assess the quality of the used model
def print_metrics(kernel):

	y_validate = split_ds()[4]

	print(metrics.classification_report(y_validate,predict_svc(kernel)))
	print(metrics.confusion_matrix(y_validate,predict_svc(kernel)))


#reduce_datasets()
split_ds()
apply_svc('linear')
predict_svc('linear')
print_metrics('linear')



# creates an isomap to visualise the classified data
#def isomap_viz():

	#x_train = split_recipeDS()[0]
	#x_iso = Isomap(n_neighbors=10).fit_transform(x_train)

	# Create a plot with subplots in a grid of 1X2
	#fig, ax = plt.subplots(1, 2, figsize=(8, 4))
