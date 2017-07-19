# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:27:15 2017

@author: AnNa
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA
#from sklearn.preprocessing import scale
from sklearn import svm
from sklearn import metrics
from sklearn.manifold import Isomap
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import cross_val_score



# it creates and fits the given svc model (linear, rbf, poly, sigmoid kernels...). it also returns the score 
def apply_svc(kern):	

	svc = svm.SVC(kernel = kern, decision_function_shape='ovr').fit(x_train, y_train)
	return svc



# predicts results of the given svc
def predict_svc():

	prediction = rbf_svc.predict(x_validate)
	return prediction


# prints the classification report of the y-validation set and the prediction. this way you can assess the quality of the used model
def print_metrics(svc):

	print("The mean accuracy on given test data and labels is: \n")
	print(svc.score(x_validate, y_validate))
	print("\n The classification report looks like this: \n")
	print(metrics.classification_report(y_validate,prediction))
	print ("\n The confusion matrix looks like this: \n" )
	print(metrics.confusion_matrix(y_validate,prediction))
	print("\n The normalized confusion matrix looks like this: \n")
	cm = metrics.confusion_matrix(y_validate,prediction)
	norm_cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	print(norm_cm)



def plot_normalized_confusion_matrix():

	cm = metrics.confusion_matrix(y_validate,prediction)
	norm_cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	print(norm_cm)
	plt.imshow(norm_cm)
	plt.title("Normalized Confusion Matrix")
	plt.colorbar()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.show()


def plot_confusion_matrix():

	cm = metrics.confusion_matrix(y_validate,predict_svc())	
	print(cm)
	plt.imshow(cm)
	plt.title("Normalized Confusion Matrix")
	plt.colorbar()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.show()


def cross_val():

	x_t, y_t = x_train.append(x_validate), np.concatenate((y_train,y_validate))

	scores = cross_val_score(rbf_svc,x_t,y_t, cv=5)
	print("\n The cross validation values are: \n")
	print(scores)

	return scores



def grid_search():

	for score in scores:

		clf = GridSearchCV(svm.SVC(), parameters, cv=5)
		clf.fit(x_train, y_train)
		# Print out the results
		print('Best score for training data: \n', clf.best_score_)
		print('Best `C`: \n',clf.best_estimator_.C)
		print('Best kernel: \n',clf.best_estimator_.kernel)
		print('Best `gamma` \n:',clf.best_estimator_.gamma)


# it reduces the dimensionality of both datasets and returns them (as numpy arrays) 
#def reduce_datasets():#	
##	
#	recipes_dataset = reduce_dimensionality(x_train)
#	ratings_dataset = reduce_dimensionality(y_train.reshape(-1, 1)	)
#	return recipes_dataset,ratings_dataset
#
## it uses pca for dimensionality reduction
#def reduce_dimensionality(dataset):
#
#	pca = PCA()
#	ds = pca.fit_transform(dataset)
#	return ds



# def plot():

# 	# create a mesh to plot in
# 	x_min, x_max = x_train[:, 0].min() - 1, x_train[:, 0].max() + 1
# 	y_min, y_max = x_train[:, 1].min() - 1, x_train[:, 1].max() + 1
# 	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))

# 	# title for the plots
# 	titles = ['SVC with linear kernel', 'SVC with RBF kernel']

# 	for i, clf in enumerate((svc, rbf_svc)):
# 		 # Plot the decision boundary. For that, we will assign a color to each
# 		 # point in the mesh [x_min, x_max]x[y_min, y_max].
# 		plt.subplot(2, 2, i + 1)
# 		plt.subplots_adjust(wspace=0.4, hspace=0.4)

# 		Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# 		# Put the result into a color plot
# 		Z = Z.reshape(xx.shape)
# 		plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

# 		# Plot also the training points
# 		plt.scatter(x_train[:, 0], x_train[:, 1], c=y_train, cmap=plt.cm.coolwarm)
# 		plt.xlabel('Sepal length')
# 		plt.ylabel('Sepal width')
# 		plt.xlim(xx.min(), xx.max())
# 		plt.ylim(yy.min(), yy.max())
# 		plt.xticks(())
# 		plt.yticks(())
# 		plt.title(titles[i])

# 	plt.show()





if __name__ == "__main__":

	recipeMatrix = pd.read_csv('recipeMatrix.csv', encoding = 'utf-8', header = None)
	ratingsNP = np.loadtxt('ratingsNP.csv')
	
	x_train, x_te, y_train, y_te = train_test_split(recipeMatrix, ratingsNP, test_size = 0.40, random_state = 42)
	x_validate, x_test, y_validate, y_test = train_test_split(x_te,y_te, test_size = 0.50, random_state = 42)

	#rm, rats = reduce_datasets()

	scores = ['linear', 'rbf']
    
    
	parameters = [{'kernel': ['rbf'], 'gamma': [0.01, 1, 100], 'C': [0.01, 1, 100]}, 
                {'kernel': ['linear'], 'C': [0.01, 1, 100]}]

	svc = apply_svc('linear')
	rbf_svc = svm.SVC(kernel='rbf', gamma = 100, decision_function_shape='ovr').fit(x_train, y_train)
	prediction = predict_svc()
	cross_val()
	print_metrics(rbf_svc)
	#grid_search()
	#plot()

	# plot_confusion_matrix()
	#plot_normalized_confusion_matrix()

