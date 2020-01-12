from Models import *

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


torch.backends.cudnn.benchmark = True
data = data.cuda()
labels = labels.cuda()
model = Tester(net_param, cls_param, dec_param).cuda()


c, x = model(data[691:711])
c = torch.argmax(c, dim=1)
la = labels[691:711]
accuracy = float((la == c).sum())
print('Accuracy:', accuracy / (20 * 5))
