#!/usr/bin/env python3
#SenseHatLogger. Author: kurtd5105

from sense_hat import SenseHat
import argparse
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
                    grouping[row][col + (i * numberDimensions[1])] = numbers[str(group[i])][row][col]
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
approximately gap seconds. The default is 1.5 seconds. Color is an rgb list, defaults to green.
"""
def displayMetrics(sense, currTemp, metric, groupings, groupingLength, rotation, gap=1, color=[0, 255, 0]):
    #X10 in the bottom 3 rows
    extraDigit = [
        [128, 128, 128],   [0, 0, 0],          [128, 128, 128],    [255, 255, 255], [0, 0, 0],
        [255, 255, 255], [255, 255, 255],   [255, 255, 255],

        [0, 0, 0],         [128, 128, 128],    [0, 0, 0],          [255, 255, 255], [0, 0, 0],
        [255, 255, 255], [0, 0, 0],         [255, 255, 255],

        [128, 128, 128],   [0, 0, 0],          [128, 128, 128],    [255, 255, 255], [0, 0, 0],
        [255, 255, 255], [255, 255, 255],   [255, 255, 255]
    ]
    #T in the bottom 3 rows
    t = [
        [0, 0, 0], [192, 192, 192],   [192, 192, 192], [192, 192, 192], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0],

        [0, 0, 0], [0, 0, 0],         [192, 192, 192], [0, 0, 0],       [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0],

        [0, 0, 0], [0, 0, 0],         [192, 192, 192], [0, 0, 0],       [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]
    ]

    #P in the bottom 3 rows
    p = [
        [0, 0, 0], [192, 192, 192],   [192, 192, 192],    [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0],

        [0, 0, 0], [192, 192, 192],   [192, 192, 192],    [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0],

        [0, 0, 0], [192, 192, 192],   [0, 0, 0],          [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]

    ]

    #H in the bottom 3 rows
    h = [
        [0, 0, 0], [192, 192, 192], [0, 0, 0],        [192, 192, 192], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0],

        [0, 0, 0], [192, 192, 192], [192, 192, 192],  [192, 192, 192], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0],

        [0, 0, 0], [192, 192, 192], [0, 0, 0],        [192, 192, 192], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0]

    ]
    sense.clear()
    sense.set_rotation(rotation)
    groups = []

    #Append the number as the whole number and then the decimal and whether it's a decimal or not
    groups.append([str(int(currTemp)), False])
    groups.append([str(currTemp - int(currTemp))[2:], True])

    #Add each metric to the display groups
    for m in metric[1]:
        groups.append([str(int(m[0])), False])
        groups.append([str(m[0] - int(m[0]))[2:], True])

    #Set the pressure to ignore the most significant digit, it is probably 1
    groups[4][0] = str(int(metric[1][1][0]) % 1000)

    overflow = [False for x in range(len(groups))]

    for i in range(8):
        if groups[i][0] == '':
            groups[i][0] = "00"
            continue
        #Check to see if any group overflows and set its overflow flag and shorten the group
        if len(groups[i][0]) > groupingLength:
            groups[i][0] = groups[i][0][0:groupingLength]
            if i % 2 == 0:
                overflow[i] = True
        #Add a 0 to the front of a non decimal, or in the back of a decimal if necessary
        elif i % 2 == 0:
            if len(groups[i][0]) == 1:
                groups[i][0] = '0' + groups[i][0]
        else:
            if len(groups[i][0]) == 1:
                groups[i][0] = groups[i][0] + '0'
    
    for i in range(8):
        sense.clear()
        #Change color accordingly here
        #Create a list of r, g, b values for each LED
        displayList = [color if groupings[groups[i][0]][row][col] else [0, 0, 0] for row in range(5) for col in range(8)]

        #If it's a decimal
        if groups[i][1]:
            displayList[32] = [255, 255, 255]

        #If there is an overflow, add the overflow signal to the screen, and move the thp indicator to the side
        if overflow[i]:
            if i < 4:
                displayList[0] = [255, 0, 0]
            elif i < 6:
                displayList[8] = [255, 255, 0]
            else:
                displayList[16] = [0, 0, 255]
            displayList.extend(extraDigit)
        #If there isn't an overflow, display the thp symbol on the bottom of the screen
        else:
            if i < 4:
                displayList.extend(t)
            elif i < 6:
                displayList.extend(p)
            else:
                displayList.extend(h)

        sense.set_pixels(displayList)
        
        time.sleep(gap)
    sense.clear()
    sense.set_rotation(0)


"""
logData
Logs all the data to a data log file, given by the dataPath.
"""
def logData(dataPath, data):
    with open(dataPath, 'a') as f:
        for point in data:
            f.write("{} Temperature: {}; Pressure: {}; Humidity: {};\n".format(*point))       


"""
logMetric
Logs the given metric to the metric log file, given by the metricPath.
"""
def logMetric(metricPath, metric):
    with open(metricPath, 'a') as f:
        f.write("{} ".format(metric[0]))
        metric1, metric2, metric3 = metric[1][0], metric[1][1], metric[1][2]
        f.write("Temperature avg: {}; min: {}; max: {}; ".format(*metric1))
        f.write("Pressure avg: {}; min: {}; max: {}; ".format(*metric2))
        f.write("Humidity avg: {}; min: {}; max: {};\n".format(*metric3))


def offHour(timerange, curr):
    if timerange[0] > timerange[1]:
        if curr.hour >= timerange[0]:
            return True
        elif curr.hour < timerange[1]:
            return True
    else:
        if curr.hour >= timerange[0] and curr.hour < timerange[1]:
            return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A Raspberry Pi Sense Hat sensor logger with LED and text file output.")
    parser.add_argument("-t", "--timerange", nargs=2, type=int, help="Optional argument to change the time range the LED matrix should be off.")
    parser.add_argument(
        "-r", "--rotation", nargs=1, type=int,
        help="Optional argument to change the LED matrix rotation in degrees. The screen will be rotated to the nearest 90 degree."
    )
    args = parser.parse_args()

    t = []
    if args.timerange:
        t = args.timerange
        for i in t:
            if i < 0 or i > 23:
                print("Time out of range, setting to default.")
                t = [23, 8]
                break
    else:
        t = [23, 8]

    rotation = 0
    if args.rotation:
        rotation = int(((round(args.rotation[0]/90, 0) % 4) * 90))

    sense = SenseHat()

    groupings = generateNumberGroupings(numbers, 2, (5, 8), (5, 4))
    now = datetime.now()
    target = datetime.now()

    #[time, [avgT, minT, maxT], [avgP, minP, maxP], [avgH, minH, maxH]]
    metric = [0, [[20, 0, 0], [1000, 0, 0], [50, 0, 0]]]
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

            #Display the current temperature and the current metrics every 2 minutes
            if i % 2 == 0:
                if not offHour(t, start):
                    displayMetrics(sense, data[-1][1], metric, groupings, 2, rotation)

            #Add a 60 second time delta from the start
            target = timedelta(seconds = 60) - (datetime.now() - start)
            delay = target.total_seconds()
            if delay < 0:
                delay = 0
            time.sleep(delay)

        start = datetime.now()
        metrics = [str(start)]
        data.append([
            str(start), 
            round(sense.get_temperature(), 2), 
            round(sense.get_pressure(), 2), 
            round(sense.get_humidity(), 2)
        ])

        #Calculate metrics here
        metric = [str(start), []]
        for i in range(1, 4):
            metricData = [d[i] for d in data]
            metric[1].append([round(sum(metricData) / len(metricData), 2), min(metricData), max(metricData)])

        print(metric)
        #Log the data and metric to log files
        logData(start.strftime("%d-%m-%Y") + "_data.log", data)
        logMetric(start.strftime("%d-%m-%Y") + "_metric.log", metric)

        target = timedelta(seconds = 60) - (datetime.now() - start)
        delay = target.total_seconds()
        if delay < 0:
            delay = 0
        time.sleep(delay)
