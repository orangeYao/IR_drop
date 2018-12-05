import torch
import torch.nn as nn
from torch.autograd import Variable
from data_wide import CustomDataset
from data_wide import weights_init
from model import CNN_single
import numpy as np

batch_size = 500
num_epochs = 200
crop_size = 15
all_size = crop_size *2 +1
learning_rate = 0.002
scale = 1

fdir1 = '../designs/design2/'
fdir2 = '../designs/design3/'
fdir3 = '../designs/design4/'
fname_test = 'ir.npy'

train_dataset = CustomDataset(fdir1, fdir2, fdir3,
                              size=crop_size)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                       batch_size=batch_size,
                                       shuffle=True,
                                       num_workers=5, drop_last=True)
channel = 1

# CNN Model (2 conv layer)
cnn = CNN_single(channel, scale, crop_size)
cnn.apply(weights_init)
cnn.cuda()

# Loss and Optimizer
criterion = nn.L1Loss()
optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)
max_pool = nn.MaxPool1d(kernel_size=50, stride=50)

# Train the model
total_step = len(train_loader)
for epoch in range(num_epochs):
    print ('epoch,', epoch)
    overall_loss = 0
    for i, (images, labels) in enumerate(train_loader):
        images = Variable(images).cuda()
        labels = torch.squeeze(labels)
        labels = Variable(labels).cuda()

        # Forward pass
        optimizer.zero_grad()

        outputs = cnn(images.view(-1, 1, all_size, all_size)) #input [10000, 1, 31, 31]
        outputs = max_pool(outputs.view(batch_size, 1, -1)) # input [500, 1, 20]

        loss = criterion(outputs.squeeze(), labels)
        loss.backward()
        optimizer.step()

        overall_loss += loss.data
    print (overall_loss)

    if epoch % 20 == 19:
        torch.save(cnn, 'cnn_234' + str(epoch // 20) + '.pkl')

