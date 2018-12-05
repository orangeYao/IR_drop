import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import math
from scipy import signal
from scipy.stats import kendalltau


fdirl = ['../designs/design1/',
         '../designs/design2/',
         '../designs/design3/',
         '../designs/design4/']
s_names = ['_one', '_two', '_three', '_four']
m_names = ['cnn_234',
           'cnn_134',
           'cnn_124',
           'cnn_123']


maxs = [0.07, 0.09, 0.06, 0.06]

def rank_kend(a, b):
    a = a.reshape(-1)
    b = b.reshape(-1)
    return (round(kendalltau(a, b)[0], 2))

def strideConv(arr, arr2, s):
    return signal.convolve2d(arr, arr2[::-1, ::-1], mode='valid')[::s, ::s]

for i in m_names:
    for idx, j in enumerate(s_names):
        name =  i + j
        result = name + '.npy'
        board = np.load(result)
        ir = np.load(irs[idx])

        b_5  = strideConv(board, np.ones((5, 5)), 5)/25
        ir_5 = strideConv(ir,    np.ones((5, 5)), 5)/25
        
        k = rank_kend(ir, board)
        k_5 = rank_kend(ir_5, b_5)

        print(name, k, ',', k_5)
#        print(name, p, r, ',', p_5, r_5, ','
#             ,round(np.percentile(ir, 95) *1000), 
#              round(np.percentile(ir_5, 95) *1000))
    print ('')


