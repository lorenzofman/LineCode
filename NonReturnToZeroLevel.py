import matplotlib.pyplot as plt
import numpy as np

highLevel = 13
lowLevel = -13

def nrzl(bits):
    encoded = []
    for bit in bits:
        if bit == 1:
            encoded.append(highLevel)
        if bit == 0:
            encoded.append(lowLevel)
    return encoded


# A string of zeros causes the NRZI data toggle each bit time, while a string
# of ones causes long period with no transition in the data. (USB NRZI)
# http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2001f/interfacing/usb/appl_note.html
def nrzi(bits):
    encoded = []
    # Check if USB starts in low/high
    low = False
    for bit in bits:
        if bit == 0:
            low = not low
        encoded.append(lowLevel if low else highLevel)
    return encoded


binary = np.array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0])
x = np.arange(0, len(binary))
y = nrzi(binary)

fig, axes = plt.subplots()

plt.setp(axes, xticks=x, xticklabels=binary, yticks=y, )
plt.step(x, y, color='#ff084a', linewidth="3", where='post')
plt.grid(color='#aaaaaa', linestyle='-', linewidth=0.5)

plt.show()
