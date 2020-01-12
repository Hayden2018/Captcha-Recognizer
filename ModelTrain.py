from Models import *
from DataProcessing import random_iterator
import time
import matplotlib.pyplot as plt

with open('captcha_data_gen', 'rb') as f:
    data = torch.load(f)
with open('captcha_label_gen', 'rb') as f:
    labels = torch.load(f)


class GeneralTrainer(nn.Module):

    def __init__(self):
        super(GeneralTrainer, self).__init__()
        self.Net = Encoder()
        self.Cls = Classifier()
        self.Dec = Decoder()
        self.CLoss = nn.CrossEntropyLoss()
        self.RLoss = nn.MSELoss()

    def forward(self, x, y):
        x1 = self.Net(x)
        x2 = self.Cls(x1)
        y = self.CLoss(x2, y)
        r = self.Dec(x1)
        r = 0.0006 * self.RLoss(r, x)
        return torch.stack([y, r])


torch.backends.cudnn.benchmark = True
data = data.cuda()
labels = labels.cuda()
train = GeneralTrainer().cuda()
Optimizer = torch.optim.Adam(train.parameters(), lr=0.0001)


s = time.time()
j = 0
x, y = [], []
for d in random_iterator(cycle=5000, iteration=5, high=44500):
    Optimizer.zero_grad()
    loss = train(data[d:d+64], labels[d:d+64]).sum()
    loss.backward()
    Optimizer.step()
    j += 1
    if j % 5 == 0:
        z = float(loss)
        print(j // 5, 'Batch completed, Loss =', z)
        x.append(j // 5)
        y.append(z)
print('Training completed, using: ', time.time() - s, 's')
plt.plot(x, y)
plt.show()


with open('Net_param', 'wb') as f:
    M = train.Net
    torch.save(M.state_dict(), f)
with open('Decode_param', 'wb') as f:
    M = train.Dec
    torch.save(M.state_dict(), f)
with open('Cls_param', 'wb') as f:
    M = train.Cls
    torch.save(M.state_dict(), f)