from Models import *
from DataProcessing import random_iterator
import time
import matplotlib.pyplot as plt

with open('captcha_data', 'rb') as f:
    data = torch.load(f)
with open('captcha_label', 'rb') as f:
    labels = torch.load(f)
with open('Net_param_gen', 'rb') as f:
    net_param = torch.load(f)
with open('Decode_param_gen', 'rb') as f:
    dec_param = torch.load(f)
with open('Cls_param_gen', 'rb') as f:
    cls_param = torch.load(f)


class TransferTrainer(nn.Module):

    def __init__(self, n_p, d_p, c_p):
        super(TransferTrainer, self).__init__()
        self.Net = Encoder()
        self.Cls = Classifier()
        self.Dec = Decoder()
        self.CLoss = nn.CrossEntropyLoss()
        self.RLoss = nn.MSELoss()
        self.Dec.load_state_dict(d_p)
        self.Net.load_state_dict(n_p)
        self.Cls.load_state_dict(c_p)

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
train = TransferTrainer(net_param, dec_param, cls_param).cuda()
Optimizer = torch.optim.Adam(train.parameters(), lr=0.00005)


s = time.time()
j = 0
x, y = [], []
for d in random_iterator(cycle=400, iteration=5, high=666):
    Optimizer.zero_grad()
    loss = train(data[d:d+24], labels[d:d+24]).sum()
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