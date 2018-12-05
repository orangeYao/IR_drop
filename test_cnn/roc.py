import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import math
from scipy import signal
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve 
from sklearn.metrics import auc 

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
        
        b_10  = strideConv(board, np.ones((10, 10)), 10)/100
        ir_10 = strideConv(ir,    np.ones((10, 10)), 10)/100
        print (name)
        print (round(roc_auc_score((ir > np.percentile(ir, 95)).reshape(-1), board.reshape(-1)), 3))
        print (round(roc_auc_score((ir_5 > np.percentile(ir_5, 95)).reshape(-1), b_5.reshape(-1)), 3))

        fpr, tpr, threshold = roc_curve((ir_5 > np.percentile(ir_5, 95)).reshape(-1), 
                                         b_5.reshape(-1))
        roc_auc = auc(fpr, tpr)
        fig = plt.figure(figsize=(12,10))
        plt.title(name, fontsize=32)
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc, linewidth=2)
        plt.legend(loc = 'lower right', fontsize=20)
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate', fontsize=20)
        plt.xlabel('False Positive Rate', fontsize=20)
        plt.gca().xaxis.set_tick_params(labelsize=18)
        plt.gca().yaxis.set_tick_params(labelsize=18)
        fig.savefig(name + '_roc', dpi=500)

        print (round(roc_auc_score((ir_10 > np.percentile(ir_10, 95)).reshape(-1), b_10.reshape(-1)), 3))

#        print(name, p, r, ',', p_5, r_5, ','
#             ,round(np.percentile(ir, 95) *1000), 
#              round(np.percentile(ir_5, 95) *1000))
    print ('')


