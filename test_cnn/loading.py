import numpy as np

##### loading
def prep(fname_train, fdir):
    tmp = [[np.load(fdir+fname_train[i])] for i in range(0, 50)]
    X = np.concatenate(tmp)
    return X

def preprocess(fdir):
    fname_train = ['Time_' + str(i) + '.npy' for i in range(1, 51)]
    fname_test = 'ir.npy'
    y = np.load(fdir+fname_test)
    X = prep(fname_train, fdir)
    return (X, y)

