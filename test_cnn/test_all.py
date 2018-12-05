import torch
import torch.nn as nn
from torch.autograd import Variable
from data_wide import CustomDataset
from data_wide import weights_init
from model import CNN_single
import numpy as np

crop_size = 15
scale = 1

fdirl = ['../designs/design1/',
         '../designs/design2/',
         '../designs/design3/',
         '../designs/design4/']
s_names = ['_one', '_two', '_three', '_four']
m_names = ['cnn_234',
           'cnn_134',
           'cnn_124',
           'cnn_123']

all_size = crop_size *2 +1
max_pool = nn.MaxPool1d(kernel_size=50, stride=50)
batch_size = 300

for j in range(4):
    fdir = fdirl[j]
    val_dataset = CustomDataset(fdir,
                                size=crop_size)
    val_loader = torch.utils.data.DataLoader(dataset=val_dataset,
                                           batch_size=batch_size,
                                           shuffle=False,
                                           num_workers=5)
    w, h, channel = val_dataset.w, val_dataset.h, val_dataset.C

    for k in range(4):
        name = m_names[k]
        cnn = CNN_single(channel, scale, crop_size)
        cnn = torch.load('../cnn/' + name + '0.pkl')

        cnn.eval()
        diff_all = np.array([])
        for i, (images, labels) in enumerate(val_loader):
            images = Variable(images).cuda()
            labels = torch.squeeze(labels)
            labels = Variable(labels).cuda()

            outputs = cnn(images.view(-1, 1, all_size, all_size)) #input [10000, 1, 31, 31]
            outputs = max_pool(outputs.view(labels.shape[0], 1, -1)) # input [500, 1, 20]

            diff_all = np.append(diff_all, outputs.data.cpu().numpy())

        board = diff_all.reshape(w, h)
        print (name + s_names[j], board.sum())
        np.save(name + s_names[j], board)

