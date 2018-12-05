import numpy as np

##### loading
def prep(fname_train, fdir):
    tmp = [[np.load(fdir+fname_train[i])] for i in range(0, 50)]
    X = np.concatenate(tmp)
    return X

def preprocess(fdir1, fdir2, fdir3):
    fname_train = ['Time_' + str(i) + '.npy' for i in range(1, 51)]
    fname_test = 'ir.npy'
    y1 = np.load(fdir1+fname_test)
    y2 = np.load(fdir2+fname_test)
    y3 = np.load(fdir3+fname_test)

    X1 = prep(fname_train, fdir1)
    X2 = prep(fname_train, fdir2)
    X3 = prep(fname_train, fdir3)
    return (X1, X2, X3, y1, y2, y3)

