# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:27:15 2017

@author: AnNa
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale


recipes = pd.read_csv('recipeMatrix.csv', encoding = 'utf-8')

print(recipes.keys())





