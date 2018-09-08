import torch
import torch.nn.functional as F
from torch import nn


# Input (N, 1, 50, 200) return (N, 4, 10, 47)
class Encoder(nn.Module):

    def __init__(self):
        super(Encoder, self).__init__()
        self.conv1 = nn.Conv2d(1, 30, 3, padding=1)
        self.conv2 = nn.Conv2d(30, 30, 2, stride=2)
        self.conv3 = nn.Conv2d(30, 20, 3, padding=1)
        self.conv4 = nn.Conv2d(20, 12, 3, padding=1)
        self.conv5 = nn.Conv2d(12, 8, kernel_size=(7, 8), stride=2)
        self.conv6 = nn.Conv2d(8, 4, 1, bias=False)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = self.conv5(x)
        x = F.relu(x)
        x = self.conv6(x)
        return x


class Classifier(nn.Module):

    def __init__(self):
        super(Classifier, self).__init__()
        self.conv1 = nn.Conv2d(4, 22, kernel_size=(10, 8))
        self.conv2 = nn.Conv1d(22, 22, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(22, 22, kernel_size=3, padding=1)
        self.fc4 = nn.Linear(880, 180)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = x.view(-1, 22, 40)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = x.view(-1, 880)
        x = self.fc4(x)
        x = x.view(-1, 36, 5)
        return x


class Decoder(nn.Module):

    def __init__(self):
        super(Decoder, self).__init__()
        self.conv1 = nn.Conv2d(4, 8, 1)
        self.conv2 = nn.ConvTranspose2d(8, 12, kernel_size=(7, 8), stride=2)
        self.conv3 = nn.Conv2d(12, 20, 3, padding=1)
        self.conv4 = nn.Conv2d(20, 30, 3, padding=1)
        self.conv5 = nn.ConvTranspose2d(30, 30, 2, stride=2)
        self.conv6 = nn.Conv2d(30, 1, 3, padding=1, bias=False)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = self.conv5(x)
        x = F.relu(x)
        x = self.conv6(x)
        return x




