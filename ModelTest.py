from Models import *
from DataProcessing import show

with open('captcha_data', 'rb') as f:
    data = torch.load(f)
with open('captcha_label', 'rb') as f:
    labels = torch.load(f)
with open('Net_param', 'rb') as f:
    net_param = torch.load(f)
with open('Decode_param', 'rb') as f:
    dec_param = torch.load(f)
with open('Cls_param', 'rb') as f:
    cls_param = torch.load(f)


gpu0 = 'cuda:0'


class Tester(nn.Module):

    def __init__(self, net_p, cls_p, dec_p):
        super(Tester, self).__init__()
        self.Net = Encoder()
        self.Net.load_state_dict(net_p)
        self.Dec = Decoder()
        self.Dec.load_state_dict(dec_p)
        self.Cls = Classifier()
        self.Cls.load_state_dict(cls_p)

    def forward(self, x):
        x = self.Net(x)
        y = self.Cls(x)
        r = self.Dec(x)
        return y, r


data = data.to(gpu0)
labels = labels.to(gpu0)
model = Tester(net_param, cls_param, dec_param).to(gpu0)


c, x = model(data[691:711])
c = torch.argmax(c, dim=1)
l = labels[691:711]
accuracy = float((l == c).sum())
print(accuracy / (20 * 5))
