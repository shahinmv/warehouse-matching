import psycopg2

import numpy as np
import pandas as pd
import torch

import matplotlib.pyplot as plt
import csv

from rbm import RBM

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
    test_set = pd.read_csv('ml-100k/u1.test', delimiter = '\t')
    
    training_set = np.array(training_set, dtype = 'int')
    test_set = np.array(test_set, dtype = 'int')


    nb_users = int(max(max(training_set[:,0]), max(test_set[:,0])))
    nb_movies = int(max(max(training_set[:,1]), max(test_set[:,1])))

    print(training_set)
    print(test_set)

    training_set = convert(training_set)
    test_set = convert(test_set)

    training_set = torch.FloatTensor(training_set)
    test_set = torch.FloatTensor(test_set)

    training_set[training_set == 0] == -1
    training_set[training_set == 1] == 0
    training_set[training_set == 2] == 0
    training_set[training_set >= 3] == 1
    test_set[test_set == 0] == -1
    test_set[test_set == 1] == 0
    test_set[test_set == 2] == 0
    test_set[test_set >= 3] == 1 

    nv = len(training_set[0])
    nh = 100
    batch_size = 943
    rbm = RBM(nv, nh)

    # Training the RBM
    nb_epoch = 10
    for epoch in range(1, nb_epoch + 1):
        train_loss = 0
        s = 0.
        for id_user in range(0, nb_users - 100, batch_size):
            vk = training_set[id_user:id_user+batch_size]
            v0 = training_set[id_user:id_user+batch_size]
            ph0,_ = rbm.sample_h(v0)
            for k in range (10):
                _,hk = rbm.sample_h(vk)
                _,vk = rbm.sample_v(hk)
                vk[v0<0] = v0[v0<0]
            phk,_ = rbm.sample_h(vk)
            rbm.train(v0,vk,ph0,phk)
            train_loss += torch.mean(torch.abs(v0[v0>=0] - vk[v0>=0]))
            s += 1.
        print('epoch: '+str(epoch)+' loss: '+str(train_loss/s))

    # Testing the RBM    
    test_loss = 0
    s = 0.
    for id_user in range(nb_users):
        v = training_set[id_user:id_user+1]
        vt = test_set[id_user:id_user+1]
        if len(vt[vt>=0]) > 0:
            _,h = rbm.sample_h(v)
            _,v = rbm.sample_v(h)
            test_loss += torch.mean(torch.abs(vt[vt>=0] - v[vt>=0]))
            s += 1.
    print('test loss: '+str(test_loss/s))

