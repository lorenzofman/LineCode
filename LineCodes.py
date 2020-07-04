import matplotlib.pyplot as plt
import numpy as np
import gc
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
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
    encoded = []
    for bit in bits:
        if bit == 0:
            encoded.append(low_level)
            encoded.append(high_level)
        else:
            encoded.append(high_level)
            encoded.append(low_level)
    return encoded


def differential_manchester(bits):
    # Todo: Study about how first bit is encoded - for now, it's encoded with manchester
    encoded = manchester([bits[0]])
    first = encoded[0]
    second = encoded[1]
    for bit in bits[1:]:
        if bit == 1:
            first, second = second, first
        encoded.append(first)
        encoded.append(second)
    return encoded


# It's using monstrous 21 GB
gc.enable()

# Todo: Fetch data from input
binary = np.array([0, 1, 0, 0, 1, 1])

# Assert that all values are bits
assert all(bit == 0 or bit == 1 for bit in binary)

# Apply line coding
y = differential_manchester(binary)

# Save values count (it may be equal to binary or the double)
count = len(y)

# Enclose with zeros (to match examples)
y.insert(0, 0)
y.insert(len(y), 0)
y.insert(len(y), 0)

# X values to follow Y values
x = np.arange(0, len(y))

# Convert binary to string list
ticks = list(map(str, binary))

# Insert first value as blank (non valid - to match examples)
ticks.insert(0, "")

# Fetch figure and axes
fig, axes = plt.subplots()

# Set Y values to display voltage
axes.yaxis.set_major_formatter(FormatStrFormatter('%dV'))

# Setup x, y and ticks
plt.setp(axes, xticks=x, xticklabels=ticks, yticks=y)

# Create fixed spaced x ticks
loc = ticker.IndexLocator(float(count) // float(len(binary)), 0)
axes.xaxis.set_major_locator(loc)

# Step function with post drawings
plt.step(x, y, color='#ff084a', linewidth="3", where='post')

# Make square graph to match examples
axes.set_ylim([low_level * -low_level / 2, high_level * high_level / 2])

# Add a nice grid
plt.grid(color='#aaaaaa', linestyle='-', linewidth=0.5)

# Display this beauty
plt.show()
