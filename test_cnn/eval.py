import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import math
from scipy import signal

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
        
        r = round(100*((
                   (ir > np.percentile(ir, 95)) & (board > np.percentile(board, 95))).sum()/
                   (ir > np.percentile(ir, 95)).sum()))
        p = round(100*((
                   (ir > np.percentile(ir, 95)) & (board > np.percentile(board, 95))).sum()/
                   (board > np.percentile(board, 95)).sum()))
        r_5 = round(100*((
                   (ir_5 > np.percentile(ir_5, 95)) & (b_5 > np.percentile(b_5, 95))).sum()/
                   (ir_5 > np.percentile(ir_5, 95)).sum()))
        p_5 = round(100*((
                   (ir_5 > np.percentile(ir_5, 95)) & (b_5 > np.percentile(b_5, 95))).sum()/
                   (b_5 > np.percentile(b_5, 95)).sum()))

        print(name, p, ',', p_5)
#        print(name, p, r, ',', p_5, r_5, ','
#             ,round(np.percentile(ir, 95) *1000), 
#              round(np.percentile(ir_5, 95) *1000))
    print ('')


