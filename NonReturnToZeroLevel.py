import matplotlib.pyplot as plt
import numpy as np
import gc
high_level = 13
mid_level = 0
low_level = -13


def nrz_l(bits):
    encoded = []
    for bit in bits:
        if bit == 1:
            encoded.append(high_level)
        if bit == 0:
            encoded.append(low_level)
    return encoded


# A string of zeros causes the NRZI data toggle each bit time, while a string
# of ones causes long period with no transition in the data. (USB NRZI)
# http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2001f/interfacing/usb/appl_note.html
def nrz_i(bits):
    encoded = []
    # Check if USB starts in low/high
    low = False
    for bit in bits:
        encoded.append(low_level if low else high_level)
        if bit == 0:
            low = not low
    return encoded


def bipolar(bits, alt_bit):
    encoded = []
    low = False
    for bit in bits:
        if bit == alt_bit:
            encoded.append(low_level if low else high_level)
            low = not low
        else:
            encoded.append(mid_level)
    return encoded


def ami(bits):
    return bipolar(bits, 1)


def pseudo_ternary(bits):
    return bipolar(bits, 0)


def manchester(bits):
    return bits


def differential_manchester(bits):
    return bits


# It's using monstrous 21 GB
gc.enable()

# Todo: Fetch data from input
binary = np.array([1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1])

# Assert that all values are bits
assert all(bit == 0 or bit == 1 for bit in binary)

# Voltage values
y = ami(binary)

# Enclose with zeros (to match examples)
y.insert(0, 0)
y.insert(len(y), 0)
y.insert(len(y), 0)

# X values to follow Y values
x = np.arange(0, len(y))

# Convert to string list
binary = list(map(str, binary))

# Insert first value as blank (non valid - to match examples)
binary.insert(0, "")

# Create and plot graph
fig, axes = plt.subplots()
plt.setp(axes, xticks=x, xticklabels=binary, yticks=y, )
plt.step(x, y, color='#ff084a', linewidth="3", where='post')
plt.grid(color='#aaaaaa', linestyle='-', linewidth=0.5)
plt.show()
