import psycopg2

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import csv

from rbm_test import RBM

conn = psycopg2.connect(
   database="d1s5qe2312f8bg", 
   user='fnqgcgvmozpmyl', 
   password='f28265da2ca5f4fddc9de7e25e5cf8c7c06c95739d5d2ce3c4275d0fb3cc922f', 
   host='ec2-54-76-43-89.eu-west-1.compute.amazonaws.com', 
   port= '5432'
)

def convert(data):
    new_data = []
    for id_users in range(1, nb_users + 1):
        id_movies = data[:,1][data[:,0] == id_users]
        id_ratings = data[:,2][data[:,0] == id_users]
        ratings = np.zeros(nb_movies)
        ratings[id_movies - 1] = id_ratings
        new_data.append(list(ratings))
    return new_data

if __name__ == "__main__":
    training_set = pd.read_csv('ml-100k/u1.base', delimiter = '\t')
    training_set = np.array(training_set, dtype = 'int')
    test_set = pd.read_csv('ml-100k/u1.test', delimiter = '\t')
    test_set = np.array(test_set, dtype = 'int')

    nb_users = int(max(max(training_set[:,0]), max(test_set[:,0])))
    nb_movies = int(max(max(training_set[:,1]), max(test_set[:,1])))

    training_set = convert(training_set)
    test_set = convert(test_set)

    training_set[training_set == 0] == -1
    training_set[training_set == 1] == 0
    training_set[training_set == 2] == 0
    training_set[training_set >= 3] == 1
    test_set[test_set == 0] == -1
    test_set[test_set == 1] == 0
    test_set[test_set == 2] == 0
    test_set[test_set >= 3] == 1 
