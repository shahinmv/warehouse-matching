import torch

class RBM():
    def __init__(self, nv, nh):
        self.W = torch.randn(nh, nv) # (hidden neurons x visible neurons) matrix for weights
        self.v_B = torch.randn(1, nv) # (1 x visible neurons) matrix for visible neurons bias
        self.h_B = torch.randn(1, nh) # (1 x hidden neurons) matrix for hidden neurons bias

    def sample_h(self, x): # x is value of visibles nodes
        wx = torch.mm(x, self.W.t()) #matrix multiplication, probabilities of hidden neurons to be activated, given v
        activation = wx + self.h_B.expand_as(wx) # sigmoid function plus bias
        p_h_given_v = torch.sigmoid(activation)  
        return p_h_given_v, torch.bernoulli(p_h_given_v) # return samples of all hidden nodes

    def sample_v(self, y): # y is hidden nodes
        wy = torch.mm(y, self.W) #matrix multiplication, probabilities of visible neurons to be activated, given h
        activation = wy + self.v_B.expand_as(wy)
        p_v_given_h = torch.sigmoid(activation)
        return p_v_given_h, torch.bernoulli(p_v_given_h) # return samples of all visible nodes

    #visible nodes after kth interation
    #probablity of hidden nodes after kth iteration
    def train(self, v0, vk, ph0, phk):
        self.W += (torch.mm(v0.t(), ph0) - torch.mm(vk.t(), phk)).t()
        #add zero to keep b as a tensor of 2 dimension
        self.v_B += torch.sum((v0 - vk), 0)
        self.h_B += torch.sum((ph0 - phk), 0)