import torch
import torch.utils.data as data
import torch.nn as nn
import numpy as np
import os
import math
import random
from loading import preprocess

def weights_init(m):
    if isinstance(m, nn.Conv2d):
        nn.init.xavier_uniform_(m.weight.data)
        nn.init.constant_(m.bias, 0.05)

class RandFlip(object):
    def __call__(self, image):
        k = np.random.randint(3)
        if k == 1:
            return np.fliplr(image) #verti [:,::-1,:]
        elif k == 2:
            return image[:,:,::-1] # horiz
        else:
            return image


class CustomDataset(data.Dataset):
    def get_index(self, index, h):
        return (int(index/h), index%h)

    def __init__(self, fdir1, fdir2, fdir3, size=5):
        self.scale = 1 
        (self.X1, self.X2, self.X3, self.y1, self.y2, self.y3) = preprocess(fdir1, fdir2, fdir3)

        self.C, self.w1, self.h1 = self.X1.shape
        self.C, self.w2, self.h2 = self.X2.shape
        self.C, self.w3, self.h3 = self.X3.shape

        self.size = size

        random.seed(3001)
        self.X1 = np.pad(self.X1, ((0, 0), (self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        self.y1 = np.pad(self.y1,     ((self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        self.X2 = np.pad(self.X2, ((0, 0), (self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        self.y2 = np.pad(self.y2,     ((self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        self.X3 = np.pad(self.X3, ((0, 0), (self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        self.y3 = np.pad(self.y3,     ((self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        #((top, bottom), (left, right))

    def __getitem__(self, index):
        #print (index)
        if index < self.w1 * self.h1:
            h = self.h1
            w = self.w1
            X = self.X1
            y = self.y1
        elif index < self.w1 * self.h1 + self.w2 * self.h2:
            index -= self.w1 * self.h1
            h = self.h2
            w = self.w2
            X = self.X2
            y = self.y2
        else:
            index -= self.w1 * self.h1 + self.w2 * self.h2
            h = self.h3
            w = self.w3
            X = self.X3
            y = self.y3

        w_x, h_y = self.get_index(index, h)

        label = y [w_x + self.scale*self.size, h_y + self.size]

        r_x, r_y = (X [:, w_x : w_x+2*self.scale*self.size+1, h_y : h_y+2*self.size+1], label) # 0, 1

        rf = RandFlip()
        r_x = rf(r_x)

        return (torch.from_numpy(r_x.copy()).type(torch.FloatTensor), 
                torch.FloatTensor([r_y]))

    def __len__(self):
        return self.w1*self.h1 + self.w2*self.h2 + self.w3*self.h3


