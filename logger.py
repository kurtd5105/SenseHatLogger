#!/usr/bin/env python3
#from sensor_hat import SenseHat
import sys
from itertools import product

#Create a dictionary for the representation of the numbers in a pixel array
numbers = {
    "0":
    [
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0]
    ],
    "1":
    [
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 0]
    ],
    "2":
    [
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0]
    ],
    "3":
    [
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0]
    ],
    "4":
    [
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ],
    "5":
    [
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0]
    ],
    "6":
    [
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0]
    ],
    "7":
    [
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ],
    "8":
    [
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0]
    ],
    "9":
    [
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0]
    ],
}

#X10 in the bottom 3 rows
extraDigit = [
    [1, 0, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1]
]

#Create an empty 8x8 array
empty = [[0 for x in range(8)] for y in range(8)]


def generateNumberGroupings(numbers, groupingLength, screenDimensions, numberDimensions):
    groupings = {}

    for group in product(range(10), repeat=groupingLength):
        grouping = [[0 for x in range(screenDimensions[1])] for y in range(screenDimensions[0])]
        #print(group)
        for i in range(groupingLength):
            for row in range(numberDimensions[0]):
                for col in range(numberDimensions[1]):
                    grouping[row][col + (i * numberDimensions[1])] = numbers[str(group[0])][row][col]
            groupings[str(group[0]) + str(group[1])] = list(grouping)

    return groupings


if __name__ == '__main__':
    #sense = SenseHat()
    groupings = generateNumberGroupings(numbers, 2, (5, 8), (5, 4))
