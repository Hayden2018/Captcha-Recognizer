import cv2 as cv
import torch
from random import randint
import os
import matplotlib.pyplot as plt


ref = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14,
       'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25, '0':26, '1':27, '2':28,
       '3':29, '4':30, '5':31, '6':32, '7':33, '8':34, '9':35}


def create_dataset():
    data = []
    label = []
    cwd = os.getcwd()
    for current, directories, files in os.walk(cwd + '\Generator\data\captcha'):
        os.chdir(current)
        for name in files:
            try:
                img = cv.imread(name, cv.IMREAD_GRAYSCALE)
                img = torch.Tensor(img)
                data.append(img)
                label.append([ref[name[i]] for i in range(5)])
            except:
                pass
    print('There are', len(data), 'data')
    data = torch.stack(data)
    data = data.view(-1, 1, 50, 200)
    label = torch.tensor(label, dtype=torch.long)
    os.chdir(os.pardir)
    with open('captcha_data_gen', 'wb') as f:
        torch.save(data, f)
    with open('captcha_label_gen', 'wb') as f:
        torch.save(label, f)


def random_iterator(cycle=60, iteration=10, high=180):
    for i in range(cycle):
        r = randint(0, high)
        for j in range(iteration):
            yield r


def show(img):
    try:
        b, g, r = cv.split(img)
        img = cv.merge([r, g, b])
        plt.imshow(img)
        plt.show()
    except:
        plt.imshow(img)
        plt.show()


def ToArray(x, type=0):
    x = x.cpu().detach()
    if type == 'image':
        if len(x.shape) == 3:
            pass
        else:
            x = x.permute(0, 2, 3, 1)
    if type == 'label':
        x = x.argmax(dim=-3)
    x = x.numpy()
    return x


if __name__ == '__main__':
    create_dataset()