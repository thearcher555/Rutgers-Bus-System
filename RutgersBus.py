#!/usr/bin/python3
from configparser import MAX_INTERPOLATION_DEPTH
from pickle import FALSE, TRUE
import random
#import numpy as np
#import matplotlib.pyplot as plt
#import tkinter as tk
#from functools import partial3

idCount = 0
idBus = 0

# status: "S" (at a stop) , "T" (in transit), "B" (taking a break)
class Bus:
    def __init__(self, num, bus_status, route):
        self.route = route
        self.num = num
        self.bus_status = str(bus_status)

class Route:
    def __init__(self, name, num_buses, stops = [], buses = []):
        self.name = str(name)
        self.stops = []
        self.buses = []
        self.num_buses = num_buses

        for x in range(self.num_buses):
            global idBus
            self.buses.append(Bus(idBus, "B", self.name))
            idBus += 1

class Stop:
    def __init__(self, name):
        self.name = name
        self.id = 0

def readRoutes(allStops = []):
    f = open("BusRoutes.txt", "r")
    lines = f.readlines()
    allRoutes = []

    for x in lines:
        x = x.strip()
        tempLine = x.split(';')
        routename = tempLine[0]
        tempLine = tempLine[1:]

        tempRoute = Route(routename, 5, [], [])
        
        for element in tempLine:
            tempStop = Stop(element)

            found = 0
            for stops in allStops:
                if stops.name == tempStop.name:
                    found = 1
                    break

            if found == 0:
                global idCount
                tempStop.id = idCount
                idCount += 1
                allStops.append(tempStop)
                tempRoute.stops.append(tempStop)
            else:
                for stops in allStops:
                    if stops.name == tempStop.name:
                        tempStop.id = stops.id
                tempRoute.stops.append(tempStop)
                           
        allRoutes.append(tempRoute)
    
    # DOUBLE the stops array of each route to make it easier to iterate through them later
    for x in allRoutes:
        length = len(x.stops)
        for i in range(length):
            x.stops.append(x.stops[i])

    return allRoutes

def initDistanceMatrix():
    global idCount
    rows = idCount + 1
    cols = idCount + 1
    distanceMatrix = [[0]*rows for i in range(cols)]
    for x in range(rows):
        for y in range(cols):
            distanceMatrix[x][y] = random.randrange(1,8)
    return distanceMatrix

def randomDistanceMatrix(distanceMatrix):
    temp = distanceMatrix
    for x in range(len(temp[0])):
        for y in range(len(temp[0])):
            temp[x][y] = random.randrange(1,8)
    return temp

def idToName(id, allRoutes = []):
    return 0

def nameToId(name, allRoutes = []):
    return 0


def findRoutes(startStop, endStop, distanceMatrix, allRoutes = []):
    possibleStops = []

    for x in allRoutes:
        found = 0
        print("checking " + x.name)
        for stops in x.stops:
            print(stops.id)
            if stops.id == int(startStop) or stops.id == int(endStop):
                found += 1
        if found >= 4:
            possibleStops.append(x.name)
    
    print("Possible routes: ")
    print(possibleStops)

allStops = []
allRoutes = readRoutes(allStops)
distanceMatrix = initDistanceMatrix()
# print(distanceMatrix)
# distanceMatrix = randomDistanceMatrix(distanceMatrix)
# print("////////////////////////////")
# print(distanceMatrix)

for x in allStops:
    print("name: " + str(x.name) + "    id: " + str(x.id))
for element in allRoutes:
    print("STOPS IN " + element.name)
    for x in element.stops:
        print(x.name)

findRoutes(0, 5, distanceMatrix, allRoutes)
    