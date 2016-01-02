#!/usr/bin/env python3
#SenseHatLogger. Author: kurtd5105

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
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1]
    ],
    "1":
    [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 1]
    ],
    "2":
    [
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 1, 1]
    ],
    "3":
    [
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 1]
    ],
    "4":
    [
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1]
    ],
    "5":
    [
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 1]
    ],
    "6":
    [
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1]
    ],
    "7":
    [
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    "8":
    [
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1]
    ],
    "9":
    [
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 1]
    ],
}


class DummySenseHat():
    def get_temperature(self):
        return 20

    def get_pressure(self):
        return 1.0

    def get_humidity(self):
        return 50

    def clear(self):
        pass


#Create an empty 8x8 array
empty = [[0 for x in range(8)] for y in range(8)]


"""
generateNumberGroupings
Generates a grid of 0 and 1 for LED off/on for each possible ordering of numbers of a
given grouping length. The grid will be of size screenDimensions, [rows, cols]. Each
number given will be of size numberDimensions, [rows, cols]. A dictionary is returned,
with the number string as the key and the display grid as its value.
"""
def generateNumberGroupings(numbers, groupingLength, screenDimensions, numberDimensions):
    groupings = {}

    #For every combination of numbers that are of groupingLength
    for group in product(range(10), repeat=groupingLength):
        #Create an empty screen
        grouping = [[0 for col in range(screenDimensions[1])] for row in range(screenDimensions[0])]

        #Copy each number onto the screen in the correct position
        for i in range(groupingLength):
            for row in range(numberDimensions[0]):
                for col in range(numberDimensions[1]):
                    grouping[row][col + (i * numberDimensions[1])] = numbers[str(group[0])][row][col]
            groupings[str(group[0]) + str(group[1])] = list(grouping)

    return groupings


"""
displayMetrics
Uses the Sense Hat to display the current temperature, as well as the hourly temperature
average, hourly pressure average, and hourly humidity average. currTemp is a float,
metric is in the standard 
[time, [avgT, minT, maxT], [avgP, minP, maxP], [avgH, minH, maxH]] format, groupings have
the strings of all possible number combinations of int groupingLength as their key and
the display grid as the value. The time each part will be displayed on screen will be
approximately gap seconds. The default is 2 seconds. Color is an rgb list, defaults to green.
"""
def displayMetrics(sense, currTemp, metric, groupings, groupingLength, gap=2, color=[0, 255, 0]):
    #X10 in the bottom 3 rows
    extraDigit = [
        [[128, 128, 128],   [0, 0, 0],          [128, 128, 128],    [192, 192, 192], [0, 0, 0],
        [192, 192, 192], [192, 192, 192],   [192, 192, 192]],

        [[0, 0, 0],         [128, 128, 128],    [0, 0, 0],          [192, 192, 192], [0, 0, 0],
        [192, 192, 192], [0, 0, 0],         [192, 192, 192]],

        [[128, 128, 128],   [0, 0, 0],          [128, 128, 128],    [192, 192, 192], [0, 0, 0],
        [192, 192, 192], [192, 192, 192],   [192, 192, 192]]
    ]
    #T in the bottom 3 rows
    t = [
        [[192, 192, 192],   [192, 192, 192], [192, 192, 192],   [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]],

        [[0, 0, 0],         [192, 192, 192], [0, 0, 0],         [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]],

        [[0, 0, 0],         [192, 192, 192], [0, 0, 0],         [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]]
    ]

    #P in the bottom 3 rows
    p = [
        [[192, 192, 192],   [192, 192, 192],    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]],

        [[192, 192, 192],   [192, 192, 192],    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]],

        [[192, 192, 192],   [0, 0, 0],          [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]]

    ]

    #H in the bottom 3 rows
    h = [
        [[192, 192, 192], [0, 0, 0],        [192, 192, 192], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]],

        [[192, 192, 192], [192, 192, 192],  [192, 192, 192], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]],

        [[192, 192, 192], [0, 0, 0],        [192, 192, 192], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]]

    ]
    sense.clear()
    groups = []

    #Append the number as the whole number and then the decimal and whether it's a decimal or not
    groups.append([str(int(currTemp)), False])
    groups.append([str(currTemp - int(currTemp)), True])

    #Add each metric to the display groups
    for m in metric[1]:
        groups.append([str(int(m[0])), False])
        groups.append([str(m[0] - int(m[0])), True])

    overflow = [False for x in range(len(groups))]

    for i in range(8):
        #Check to see if any group overflows and set its overflow flag and shorten the group
        if len(groups[i][0]) > groupingLength:
            groups[i][0] = groups[i][0][0:groupingLength]
            overflow[i] = True
        #Add a 0 to the front of a non decimal, or in the back of a decimal if necessary
        elif i % 2 == 0:
            if len(groups[i][0]) == 1:
                groups[i][0] = '0' + groups[i][0]
        else:
            if len(groups[i][0]) == 1:
                groups[i][0] = groups[i][0] + '0'

        
    
    for i in range(8):
        #Change color accordingly here
        #Create a list of r, g, b values for each LED
        displayList = [[color if groupings[groups[i][0]][row][col] else [0, 0, 0] for col in range(8)] for row in range(5)]

        #If it's a decimal
        if groups[i][1]:
            displayList[4][0] = [255, 255, 255]

        #If there is an overflow, add the overflow signal to the screen, and move the thp indicator to the side
        if overflow[i]:
            if i < 4:
                displayList[0][0] = [255, 0, 0]
            elif i < 6:
                displayList[1][0] = [255, 255, 0]
            else:
                displayList[2][0] = [0, 0, 255]
            displayList.extend(extraDigit)
        #If there isn't an overflow, display the thp symbol on the bottom of the screen
        else:
            if i < 4:
                displayList.extend(t)
            elif i < 6:
                displayList.extend(p)
            else:
                displayList.extend(h)

        #print(displayList)
        #sense.set_pixels(displayList)
        
        time.sleep(gap)


if __name__ == '__main__':
    #sense = SenseHat()
    sense = DummySenseHat()
    groupings = generateNumberGroupings(numbers, 2, (5, 8), (5, 4))
    now = datetime.now()
    target = datetime.now()

    #[time, [avgT, minT, maxT], [avgP, minP, maxP], [avgH, minH, maxH]]
    metric = [0, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    while True:
        data = []

        #From t 0 to 59 
        for i in range(60):
            start = datetime.now()
            #Print the current time for debug purposes
            print(start)

            #Take measurements
            data.append([
                str(start), 
                round(sense.get_temperature(), 2), 
                round(sense.get_pressure(), 2), 
                round(sense.get_humidity(), 2)
            ])

            #Display the current temperature and the current metrics
            displayMetrics(sense, data[-1][1], metric, groupings, 2)

            #Add a 60 second time delta from the start
            target = timedelta(seconds = 60) - (datetime.now() - start)
            time.sleep(target.total_seconds())

        start = datetime.now()
        metrics = [str(start)]
        data.append([
            str(start), 
            round(sense.get_temperature(), 2), 
            round(sense.get_pressure(), 2), 
            round(sense.get_humidity(), 2)
        ])

        #Calculate metrics here
        metric = [str(start)]
        for i in range(1, 4):
            metricData = [d[i] for d in data]
            metric.append([sum(metricData) / len(metricData), min(metricData), max(metricData)])
        metrics.append(metric)

        #Display the current temperature and the current metrics
        displayMetrics(sense, data[-1][1], metric, groupings, 2)

        #Log metrics and data here

        target = timedelta(seconds = 60) - (datetime.now() - start)
        time.sleep(target.total_seconds())
