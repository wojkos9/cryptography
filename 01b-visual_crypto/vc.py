import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from random import random
import os

DIR = os.path.dirname(os.path.realpath(__file__))

img = io.imread(f"{DIR}/input.png")
if len(img.shape) > 2:
    img = img[:,:,0]

def make_shares(img: np.ndarray):
    a = [[0, 1],
         [1, 0]]
    b = [[1, 0],
         [0, 1]]
    c = [[0, 1],
         [0, 1]]
    d = [[1, 0],
         [1, 0]]
    p, p_r = (a, b), (b, a)
    q, q_r = (c, d), (d, c)
    mm = ((p, p_r), (q, q_r))

    w, h = img.shape[:2]
    mi, ma = np.min(img), np.max(img)
    th = (mi + ma) / 2
    s1, s2 = [np.ndarray((w*2, h*2)) for _ in range(2)]
    for i in range(w):
        for j in range(h):
            x, y = i*2, j*2
            m, m_r = mm[random() < 0.5]
            r = (slice(x, x+2), slice(y, y+2))
            ch = random() < 0.5
            if img[i][j] < th:  # black pixel => different b/w pairs
                a1, b1 = m if ch else m_r
                s1[r] = a1
                s2[r] = b1
            else:               # white pixel => same b/w pair
                a1 = m[ch]
                s1[r] = a1
                s2[r] = a1

    return s1, s2

s1, s2 = make_shares(img)
j = np.clip(s1 + s2, 0, 1)

for img, title in ((s1, "Share 1"), (s2, "Share 2"), (j, "Together")):
    plt.title(title)
    plt.imshow(img, cmap='gray_r')
    plt.colorbar()
    plt.show()
