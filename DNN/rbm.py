import numpy as np
import tensorflow as tf

class RBM(object):
    def __init__(self, visibleNeurons, epochs=20, hiddenNeurons=50, ratingValues=10, learningRate=0.001, batchSize=100):

        self.visibleDimensions = visibleNeurons
        self.epochs = epochs
        self.hiddenDimensions = hiddenNeurons
        self.ratingValues = ratingValues
        self.learningRate = learningRate
        self.batchSize = batchSize