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
        nn.init.xavier_uniform(m.weight.data)
        nn.init.constant(m.bias, 0.05)

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

    def __init__(self, fdir, size=5):
        self.scale = 1
        (self.X, self.y) = preprocess(fdir)

        self.C, self.w, self.h = self.X.shape

        self.size = size

        random.seed(3001)
        self.X = np.pad(self.X, ((0, 0), (self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')
        self.y = np.pad(self.y,     ((self.scale*self.size, self.scale*self.size), (self.size, self.size)), 'constant')

    def __getitem__(self, index):
        h = self.h
        w = self.w
        X = self.X
        y = self.y

        w_x, h_y = self.get_index(index, h)

        label = y [w_x + self.scale*self.size, h_y + self.size]

        r_x, r_y = (X [:, w_x : w_x+2*self.scale*self.size+1, h_y : h_y+2*self.size+1], label) # 0, 1

        return (torch.from_numpy(r_x.copy()).type(torch.FloatTensor), 
                torch.FloatTensor([r_y]))

    def __len__(self):
        return self.w*self.h


