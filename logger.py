#!/usr/bin/env python3
#from sensor_hat import SenseHat
import sys
import time
from datetime import datetime
from datetime import timedelta
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


class DummySenseHat():
    def get_temperature(self):
        return 20

    def get_pressure(self):
        return 1.0

    def get_humidity(self):
        return 50


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
    sense = DummySenseHat()
    groupings = generateNumberGroupings(numbers, 2, (5, 8), (5, 4))
    now = datetime.now()
    target = datetime.now()
    metric = [0, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    while True:
        data = []

        #From t 0 to 59 
        for i in range(60):
            start = datetime.now()
            #print(start)
            #Take measurements
            data.append([str(start), sense.get_temperature(), sense.get_pressure(), sense.get_humidity()])

            #Display measurements here

            #Add a 60 second time delta from the start
            target = timedelta(seconds = 60) - (datetime.now() - start)
            time.sleep(target.total_seconds())

        start = datetime.now()
        metrics = [str(start)]
        data.append([str(start), sense.get_temperature(), sense.get_pressure(), sense.get_humidity()])

        #Calculate metrics here
        metric = []
        for i in range(1, 4):
            metricData = [d[i] for d in data]
            metric.append([sum(metricData) / len(metricData), min(metricData), max(metricData)])
        metrics.append(metric)
        #print(metrics)

        #Log metrics and data here

        target = timedelta(seconds = 60) - (datetime.now() - start)
        time.sleep(target.total_seconds())
