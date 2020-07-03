import matplotlib.pyplot as plt
import numpy as np

highLevel = 13
lowLevel = -13


def nrlz(bit):
    if bit == 1:
        return highLevel
    if bit == 0:
        return lowLevel
    raise Exception()


binary = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1, 0])
x = np.arange(0, len(binary))
y = list(map(nrlz, binary))
plt.xticks(x, binary)
plt.yticks([lowLevel, highLevel])
plt.step(x, y, color='#ff084a', linewidth="3", where='post')
plt.grid(color='#aaaaaa', linestyle='-', linewidth=1)
plt.show()
