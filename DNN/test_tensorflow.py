#Tensorflow library. Used to implement machine learning models
import tensorflow as tf
#Numpy contains helpful functions for efficient mathematical calculations
import numpy as np
#Dataframe manipulation library
import pandas as pd
#Graph plotting library
import matplotlib.pyplot as plt


movies_df = pd.read_csv('ml-1m/movies.dat', sep='::', header=None, engine='python')
print(movies_df)
