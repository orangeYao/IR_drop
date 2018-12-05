import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import math

def plot(board, name, vmax):
    fig = plt.figure(figsize=(12,10))
    ax = plt.gca()
    ax.set_aspect('equal')
    masked_array = np.ma.array (board, mask=board < 0.01*board.mean())
    cmap = matplotlib.cm.jet
    cmap.set_bad('white',1.)
    plt.imshow(np.flipud(np.rot90(masked_array)), origin='lower', vmax = min(vmax, board.max()*2), cmap = cmap)
    plt.colorbar(orientation="vertical", pad=0.1)
    plt.title(name, fontsize=22)
    fig.savefig(name, dpi=500)
    plt.clf()
    plt.close(fig)


irs = ['../time1/coarse/ir.npy',
         '../time2/coarse/ir.npy',
         '../time3/coarse/ir.npy',
         '../time4/coarse/ir.npy']
s_names = ['_one', '_two', '_three', '_four']
m_names = ['pool_15_234',
           'pool_15_134',
           'pool_15_124',
           'pool_15_123']


maxs = [0.07, 0.09, 0.06, 0.06]

for i in m_names:
    for idx, j in enumerate(s_names):
        name =  i + j
        result = name + '.npy'
        board = np.load(result)
        plot(board, name, vmax = maxs[idx])

        ir = np.load(irs[idx])
        loss = np.abs(ir - board).sum()/board.size * 1000
        rms = math.sqrt(((ir - board)**2).sum()/board.size) * 1000
        bias = (ir - board).sum()/board.size * 1000
        
        s1 = int(round(100*((
                   (ir > np.percentile(ir, 99)) & (board > np.percentile(board, 90))).sum()/
                   (ir > np.percentile(ir, 99)).sum())))
        s2 = int(round(100*((
                   (ir > np.percentile(ir, 95)) & (board > np.percentile(board, 90))).sum()/
                   (ir > np.percentile(ir, 95)).sum())))
        print(name, round(s1), round(s2), round(loss, 2), round(rms, 2), 
                    round(1000*ir.mean(),2), round(bias, 1))
    print ('')


