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


# creates a numpy array with recipes out of the dataframe 
dataset = pd.read_csv('recipeMatrix.csv', encoding = 'utf-8')

# it splits the dataframe into
train, validate, test = np.split(dataset.sample(frac=1), [int(.6*len(dataset)), int(.8*len(dataset))])

# it creates the numpy array for the train data
training_recipes = train.as_matrix()

# it creates the numpy array for the validation data
validation_recipes = validate.as_matrix()

# it creates the numpy array for the test data
test_recipes = test.as_matrix()



# creates pca for dimentionality reduction. no parameters, cause all components should be kept
pca = PCA()

# reduces the dataset´s dimensionality 
recipes = pca.fit_transform(data)





# class labels = chefkoch sterne
cat = [1,2,3,4,5]

# this returns a shape
classifier = svm.LinearSVC(decision_function_shape='ovr')

# Fit the SVM model according to the given training data.
classifier.fit(train, cat)





