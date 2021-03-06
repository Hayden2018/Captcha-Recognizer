from DataProcessing import *
from Models import *
from CaptchaReducer import *


with open('Net_param', 'rb') as f:
    net_param = torch.load(f, map_location='cpu')
with open('Cls_param', 'rb') as f:
    cls_param = torch.load(f, map_location='cpu')
ref = {v: k for k, v in ref.items()}
Net = Encoder()
Net.load_state_dict(net_param)
Cls = Classifier()
Cls.load_state_dict(cls_param)
reducer = CaptchaReducer('background.png')


def getIMG(name):
    img = cv.imread(name, cv.IMREAD_COLOR)
    img = reducer(img)
    return img


# (50*200 Pytorch Tensor) return string
def recognize(x):
    x = x.view(1, 1, 50, 200)
    x = Net(x)
    y = Cls(x)
    y = torch.argmax(y, dim=1)
    y = y.view(5)
    ans = ''
    for i in range(5):
        ans += ref[float(y[i])]
    return ans


if __name__ == '__main__':
    img = getIMG('captcha.png')
    img = torch.tensor(img)
    print(recognize(img))
    img = ToArray(img)
    img = img.reshape(50, 200)
    show(img)
