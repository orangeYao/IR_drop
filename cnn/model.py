import torch
import torch.nn as nn
from torch.autograd import Variable

class CNN_single(nn.Module):
    def __init__(self, channel, scale, crop_size):
        super(CNN_single, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(channel, 16, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU())
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 16, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU())
        self.layer3 = nn.Sequential(
            nn.Conv2d(16, 8, kernel_size=3, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU())
        self.layer4 = nn.Sequential(
            nn.Conv2d(8, 8, kernel_size=3, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU())

        l_size = int((crop_size *2 +1)/2 /2) # 7-4 = 3
        l_size2 = int((scale*crop_size *2 +1) /2 /2)
        self.fc = nn.Linear(l_size*l_size2*8, l_size*l_size2)
        self.fc2 = nn.Linear(l_size*l_size2, 1)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        out = self.fc2(out)
        return out
