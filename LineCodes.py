import matplotlib.pyplot as plt
import numpy as np
import gc
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker

high_level = 5
mid_level = 0
low_level = -5


# O protocolo RS-232 define uma faixa de tensões para considerar os sinais, sendo elas:
# – -3 V a -15V como Marca = 1 = OFF
# – +3V a +15V como Espaço = 0 = ON (Pronto)
# Optamos por considerar um valor médio entre o máximo e minimo definidos, sendo então -9 e 9 volts
def nrz_l(bits):
    encoded = []
    for bit in bits:
        if bit == 1:
            encoded.append(low_level)
        if bit == 0:
            encoded.append(high_level)
    return encoded


# A string of zeros causes the NRZI data toggle each bit time, while a string
# of ones causes long period with no transition in the data. (USB NRZI)
# http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2001f/interfacing/usb/appl_note.html
# The USB protocol use bit-stuffing after every sequence of six '1', but we don't implement this here
def nrz_i(bits):
    encoded = []
    # Check if USB starts in low/high
    low = True
    for bit in bits:
        if bit == 1:
            low = not low
        encoded.append(high_level if low else low_level)
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
            encoded.append(high_level)
            encoded.append(low_level)
        else:
            encoded.append(low_level)
            encoded.append(high_level)
    return encoded


def differential_manchester(bits):
    encoded = []
    first = low_level
    second = high_level
    for bit in bits:
        if bit == 0:
            encoded.append(first)
            encoded.append(second)
        else:
            first, second = second, first
            encoded.append(first)
            encoded.append(second)
    return encoded


from enum import Enum


class LineCode(Enum):
    nrz_l = 1
    nrz_i = 2
    ami = 3
    pseudo_ternary = 4
    manchester = 5
    differential_manchester = 6


# It's using monstrous 21 GB
gc.enable()

# Todo: Fetch data from input

print("The sequence should be input in the format: '1 0 1 0 1 0 0', without quotes and every bit separated by a space")
binary = list(map(int, input("\nEnter binary sequence: ").strip().split()))

# Assert that all values are bits
assert all(bit == 0 or bit == 1 for bit in binary)

lineCoding = int(input(
    "Select line coding: \n1 - nrz_l;\n2 - nrz_i;\n3 - ami;\n4 - pseudo_ternary;\n5 - manchester;\n6 - differential "
    "manchester;\nLine code:"))

y = []
if LineCode(lineCoding) == LineCode.nrz_l:
    y = nrz_l(binary)
elif LineCode(lineCoding) == LineCode.nrz_i:
    y = nrz_i(binary)
elif LineCode(lineCoding) == LineCode.ami:
    y = ami(binary)
elif LineCode(lineCoding) == LineCode.pseudo_ternary:
    y = pseudo_ternary(binary)
elif LineCode(lineCoding) == LineCode.manchester:
    y = manchester(binary)
elif LineCode(lineCoding) == LineCode.differential_manchester:
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
