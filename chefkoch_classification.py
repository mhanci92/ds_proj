# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:27:15 2017

@author: AnNa
"""
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd

#from sklearn.decomposition import PCA
#from sklearn.preprocessing import scale
from sklearn import svm
from sklearn import metrics
#from sklearn.manifold import Isomap
from sklearn.model_selection import train_test_split



# it creates and fits the given svc model (linear, rbf, poly, sigmoid kernels...). it also returns the score 
def apply_svc():	

	svc = svm.SVC(kernel = "linear", decision_function_shape='ovr').fit(x_train, y_train)
	print(svc.score(x_validate, y_validate))
	return svc



# predicts results of the given svc
def predict_svc():

	prediction = apply_svc().predict(x_validate)

	print(prediction)
	print(y_validate)

	return prediction


# prints the classification report of the y-validation set and the prediction. this way you can assess the quality of the used model
def print_metrics():

	print(metrics.classification_report(y_validate,predict_svc()))
	print(metrics.confusion_matrix(y_validate,predict_svc()))



#reduce_datasets()


# creates an isomap to visualise the classified data
#def isomap_viz():

	#x_train = split_recipeDS()[0]
	#x_iso = Isomap(n_neighbors=10).fit_transform(x_train)

	# Create a plot with subplots in a grid of 1X2
	#fig, ax = plt.subplots(1, 2, figsize=(8, 4))


# it reduces the dimensionality of both datasets and returns them (as numpy arrays) 
#def reduce_datasets():#	
#	
#	recipes_dataset = reduce_dimensionality(recipeMatrix.shape)	
#	ratings_dataset = reduce_dimensionality(ratingsDF.shape)
#	return recipes_dataset,ratings_dataset

# it uses pca for dimensionality reduction
#def reduce_dimensionality(dataset):

#	pca = PCA()
#	ds = pca.fit_transform(dataset)
#	return ds


if __name__ == "__main__":
	recipeMatrix = pd.read_csv('recipeMatrix.csv', encoding = 'utf-8', header = None)
	ratingsNP = np.loadtxt('ratingsNP.csv')
	x_train, x_te, y_train, y_te = train_test_split(recipeMatrix, ratingsNP, test_size = 0.40, random_state = 42)
	x_validate, x_test, y_validate, y_test = train_test_split(x_te,y_te, test_size = 0.50, random_state = 42)

	apply_svc()
	predict_svc()
	print_metrics()

