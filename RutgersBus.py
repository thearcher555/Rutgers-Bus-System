#!/usr/bin/python3
from configparser import MAX_INTERPOLATION_DEPTH
from pickle import FALSE, TRUE
import random
import sys
import time
from tkinter import *
#import numpy as np
#import matplotlib.pyplot as plt
#import tkinter as tk
#from functools import partial3

idCount = 0
idBus = 0
allBuses = []
speed = 0.25

# status: "S" (at a stop) , "T" (in transit), "B" (taking a break)
class Bus:
    location = 0
    def __init__(self, num, bus_status, route):
        self.route = route
        self.num = num
        self.bus_status = str(bus_status)
        global allBuses
        allBuses.append(self)

    def incrementLocation(self):
        self.location += 1

class Route:
    def __init__(self, name, num_buses, stops = [], buses = []):
        self.name = str(name)
        self.stops = []
        self.buses = []
        self.num_buses = num_buses
        self.length = 0

        for x in range(self.num_buses):
            global idBus
            self.buses.append(Bus(idBus, "B", self.name))
            idBus += 1

class Stop:
    def __init__(self, name):
        self.name = name
        self.id = 0
        self.location = 0


class Display:
    def __init__(self, root, distanceMatrix, allStops, allRoutes):
        self.stopList = []
        for x in allStops:
            self.stopList.append(x.name)
        #print(stopList)
        self.distanceMatrix = distanceMatrix
        self.allStops = allStops
        self.allRoutes = allRoutes
        self.lbl1=Label(root, text='Start Stop')
        self.lbl2=Label(root, text='Destination Stop')
        #self.lbl3=Label(root, text='f')
       #self.lbl4=Label(root, text='')
        self.lbl5=Label(root, text='')#result title
        self.lbl6=Label(root, text='')#result
        self.t1=Entry(bd=3)
        self.t2=Entry(bd=3)
        #self.t3=Entry(bd=3)

        # self.btn1 = Button(root, text='Get Route')
        # self.btn2 = Button(root, text='Display Dashboard')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        #self.lbl3.place(x=50, y=150)
        #self.t3.place(x=200, y=150)

        self.b1= Button(root, text='Get Route', command=self.getRoute)
        self.b2= Button(root, text='Display Dashboard + Optimize Routes', command=self.getDash)
        self.b3= Button(root, text='Increment Time (5 Minutes)', command=self.kawamami)
        self.b1.pack()
        self.b2.pack()
        self.b3.pack()
        self.b1.place(x=100, y=250)
        self.b2.place(x=175, y=250)
        self.b3.place(x=400, y=250)
        self.lbl5.place(x=100, y=300)
        self.lbl6.place(x=200, y=300)

    def getRoute(self):
        self.lbl5.config(text = "Fastest Route")
        stop1 = str(self.t1.get())
        stop2 = str(self.t2.get())
        try:
            if checkStop(stop1, allStops) == False:
                raise Exception("You have entered in an invalid stop. Please try again.")
                    
            if checkStop(stop2, allStops) == False:
                raise Exception("You have entered in an invalid stop. Please try again.")

            bestRt = findBestRoute(nameToId(stop1, allStops), nameToId(stop2, allStops), "", "P", 0.2, self.distanceMatrix, self.allStops, self.allRoutes)
            self.lbl6.config(text = bestRt)
        except:
            self.lbl6.config(text = "Invalid Input\nPlease Check Inputs and Resubmit")

    def getDash(self):
        self.lbl6.config(text = "Dashboard")
        output = dashboard(self.distanceMatrix, self.allStops, self.allRoutes)
        if not output == '':
            self.lbl6.config(text = output)

    def kawamami(self):
        self.distanceMatrix = randomDistanceMatrix(distanceMatrix, allRoutes)
        for routes in allRoutes:
            moveBuses(routes)
        
         


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

def initDistanceMatrix(allRoutes = []):
    global idCount
    rows = idCount + 1
    cols = idCount + 1
    distanceMatrix = [[0]*rows for i in range(cols)]
    for x in range(rows):
        for y in range(cols):
            distanceMatrix[x][y] = random.randrange(3, 6)

    for x in allRoutes:
        current = 0
        index = 0
        for i in range(int(len(x.stops)/2)):
            
            if i == 0:
                x.stops[i].location = 0

            else:
                prevIndex = i - 1
                value = distanceMatrix[x.stops[prevIndex].id][x.stops[i].id]
                current += value
                x.stops[i].location = current  
            index = i

        x.length = current + distanceMatrix[x.stops[index].id][x.stops[0].id]

    return distanceMatrix

def randomDistanceMatrix(distanceMatrix, allRoutes = []):
    temp = distanceMatrix
    for x in range(len(temp[0])):
        for y in range(len(temp[0])):
            temp[x][y] = random.randrange(1,8)
    
    for x in allRoutes:
        current = 0
        index = 0
        for i in range(int(len(x.stops)/2)):
            
            if i == 0:
                x.stops[i].location = 0

            else:
                prevIndex = i - 1
                value = distanceMatrix[x.stops[prevIndex].id][x.stops[i].id]
                current += value
                x.stops[i].location = current  
            index = i

        x.length = current + distanceMatrix[x.stops[index].id][x.stops[0].id]
    return temp

#stop id to name
def idToName(id, allStops = []):
    name = ""
    for x in allStops:
        if x.id == int(id):
            name = x.name
    return name

def nameToId(name, allStops = []):
    id = 0
    for x in allStops:
        if x.name == name:
            id = x.id
    return id

#returns route object based on name
def returnRoute(name, allRoutes = []):
    for x in allRoutes:
        if x.name == name:
            return x

def printRoute(name, allRoutes = []):
    route = returnRoute(name, allRoutes)
    print("Route: " + route.name + ", Length: " + str(route.length))
    print("_______________________")
    for x in route.stops:
        print(x.name + ", Location; " + str(x.location))

#find routes accesible from stopID
def findRoutes(startStop, endStop, distanceMatrix, allRoutes = []):
    possibleRoutes = []

    for x in allRoutes:
        found = 0
        
        for stops in x.stops:
            
            if stops.id == int(startStop) or stops.id == int(endStop):
                found += 1
        if found >= 4:
            possibleRoutes.append(x.name)
    return possibleRoutes

def moveBuses(route):
    length = route.length

    for bus in route.buses:
        bus.location += 5

        if bus.location > length:
            bus.location = bus.location - length

def checkStop(input, allStops = []):
    bool = False
    for x in allStops:
        #print("comparing " + str(input) + " to " + x.name)
        if input == x.name:
            bool = True
            break
    return bool

def distributeBuses(num, allRoutes = []):
    for routes in allRoutes:
        length = routes.length
        temp = int(length/num)
        counter = 0

        for i in range(num):
            if counter > routes.length:
                counter = abs(counter - routes.length)
            routes.buses[i].location = counter
            counter += temp

def speedUpRoute(route, distanceMatrix):
    newTime = 0
    global speed
    global idBus
    speed = 0.2
        
    for i in range(int(len(route.stops)/2)):
        temp = int(distanceMatrix[route.stops[i].id][route.stops[i+1].id] * (1-speed))
        distanceMatrix[route.stops[i].id][route.stops[i+1].id] = temp
        newTime += temp

    if len(route.buses) < 8:
        temp = Bus(idBus, "B", route.name)
        temp.locaiton = 0
        route.buses.append(temp)
        print("              *** Adding bus to Route " + route.name + " ***")
        idBus += 1

    return newTime


# mode F -> just return how long it will take, mode P -> print information
def findBestRoute(startStop, endStop, route, mode, speed, distanceMatrix, allStops = [], allRoutes = []):
    estTime = 0
    bestRoute = ""
    bestRouteObj = 0
    if route != "":
        bestRouteObj = returnRoute(route, allRoutes)
        x = 0
        y = int(endStop)
        while x != y:
            dm_x = bestRouteObj.stops[x].id
            dm_y = bestRouteObj.stops[x+1].id
                
            estTime += distanceMatrix[dm_x][dm_y]
            x += 1
    else:
        estimatedTime = sys.maxsize
        possibleRoutes = findRoutes(startStop, endStop, distanceMatrix, allRoutes)
        for element in possibleRoutes:
            route = returnRoute(element, allRoutes)
            startIndex = 0
            endIndex = 0
            
            for x in range(len(route.stops)):
                if route.stops[x].id == int(startStop):
                    startIndex = x
                if route.stops[x].id == int(endStop):
                    endIndex = x
                if startIndex != 0 and endIndex > startIndex:
                    break
            #print("start at: " + str(startIndex) +" end at: " + str(endIndex))
            # need to calculate "estimated time" from distance vector here
            x = startIndex
            y = endIndex
            while x != y:

                # if (x  == len(route.stops)-1):
                #     nextStop = 0
                # else:
                #     nextStop = x+1

                dm_x = route.stops[x].id
                dm_y = route.stops[x+1].id
                
                estTime += distanceMatrix[dm_x][dm_y]
                x += 1

            if estTime < estimatedTime:
                estimatedTime = estTime
                bestRoute = element
        bestRouteObj = returnRoute(bestRoute, allRoutes)

    closestBus = 0
    closestBusDistance = sys.maxsize
    startLocation = 0

    if mode == "P":
        for stops in allStops:
            if int(startStop) == stops.id:
                startLocation = stops.location
                break
    else:
        startLocation = 0


    for buses in bestRouteObj.buses:
        #print("Bus " + str(buses.num) + ", at location: " + str(buses.location))
        temp1 = abs(startLocation - buses.location)
        temp2 = bestRouteObj.length - buses.location + startLocation

        if temp1 < closestBusDistance:
            closestBusDistance = temp1
            closestBus = buses.num
        if temp2 < closestBusDistance:
            closestBusDistance = temp2
            closestBus = buses.num

    totalTripTime = estTime + closestBusDistance
    output =''
    if mode == "P":   
        print("Origin: " + str(idToName(int(startStop), allStops))) 
        print("Destination: " + str(idToName(int(endStop), allStops)))
        print("Fastest Route: " + route.name + " (" + str(estTime) + " minutes)")  
        print("Nearest Bus: #" + str(closestBus) + ", " + str(closestBusDistance) + " minute(s) away")
        print("TOTAL TRIP TIME: " + str(totalTripTime))
        output += "Origin: " + str(idToName(int(startStop), allStops)) + "\nDestination: " + str(idToName(int(endStop), allStops)) + "\nFastest Route: " + route.name + " (" + str(estTime) + " minutes)"+  "\nNearest Bus: #" + str(closestBus) + ", " + str(closestBusDistance) + " minute(s) away"+"\nTOTAL TRIP TIME: " + str(totalTripTime)
        print(output)
        return output
        # return totalTripTime

    if totalTripTime > 30:
        # ADD BUS IN SPEED ROUTE
        print("*** The " + bestRouteObj.name + " route took " + str(totalTripTime) + " minutes to traverse. Speeding up route. ***")
        totalTripTime = speedUpRoute(bestRouteObj, distanceMatrix)
        return totalTripTime

    return totalTripTime
    
# this isn't done yet
def dashboard(distanceMatrix = [], allStops = [], allRoutes = []):
    slowRoutes = []
    global allBuses
    output=''
    # print(" ----- Dashboard -----")
    # print("# Active Buses: " + str(len(allBuses)))
    output += "# Active Buses: " + str(len(allBuses)) + "\n"
    for routes in allRoutes:
        speed = 0.20
        time = findBestRoute(0, int(len(routes.stops)/2), routes.name, "F", speed, distanceMatrix, allStops, allRoutes)
        output+=str("Route " + routes.name + " | " + str(len(routes.buses)) + " Active Buses | Length of Route: " + str(time) + " minutes\n") 

    return output

# def simulate():
#     input("Welcome to the Rutgers Bus Controller. Press Enter to initialize and continue...")
#     allStops = []
#     allRoutes = readRoutes(allStops)
#     print("\nReading routes and stops from text files...")
#     time.sleep(.5)
#     print("\n     Initializing distances...")
#     distanceMatrix = initDistanceMatrix(allRoutes)
#     time.sleep(.5)
#     print("\n             Distributing buses along routes...\n")
#     distributeBuses(5, allRoutes)

#     # probably put some kind of try catch here??
#     while 1:
#         userInput = ""
#         while 1:
#             userInput = input("\nOptions: D (See Dashboard), TR (Transport Request), C (Continue Simulation by 5 minutes), E (Exit Program)\n")
#             if userInput != 'D' and userInput != 'TR' and userInput != 'C' and userInput != 'E':
#                 print("Invalid input, try again!")
#                 continue
#             break
        
#         if userInput == 'E':
#             print("Exiting...")
#             time.sleep(.5)
#             sys.exit()
#         elif userInput == 'C':
#             distanceMatrix = randomDistanceMatrix(distanceMatrix, allRoutes)
#             for routes in allRoutes:
#                 moveBuses(routes)
#         elif userInput == 'D':
#             dashboard(distanceMatrix, allStops, allRoutes)
                    
#         elif userInput == "TR":
#             try:
#                 origin = input("\nEnter your current stop:")
#                 if checkStop(origin, allStops) == False:
#                     print("You have entered in an invalid stop. Please try again.")
#                     continue
#                 destination = input("Enter your intended destination:")
#                 if checkStop(destination, allStops) == False:
#                     print("You have entered in an invalid stop. Please try again.")
#                     continue
#                 print()
#                 findBestRoute(nameToId(origin, allStops), nameToId(destination, allStops), "", "P", 0, distanceMatrix, allStops, allRoutes)
#             except:
#                 print("Invalid input. Make sure that a route exists between your inputted stops.")

if __name__ == "__main__":
    # simulate()
    # print("Welcome to the Rutgers Bus Controller.")
    # #input("Welcome to the Rutgers Bus Controller. Press Enter to initialize and continue...")
    # allStops = []
    # allRoutes = readRoutes(allStops)
    # print("\nReading routes and stops from text files...")
    # time.sleep(.5)
    # print("\n     Initializing distances...")
    # distanceMatrix = initDistanceMatrix(allRoutes)
    # time.sleep(.5)
    # print("\n             Distributing buses along routes...\n")
    # distributeBuses(5, allRoutes)

    allStops = []
    allRoutes = readRoutes(allStops)
    distanceMatrix = initDistanceMatrix(allRoutes)
    distributeBuses(5, allRoutes)

    root = Tk()
    root.title = ('Bus Route Selector')
    disp = Display(root, distanceMatrix, allStops, allRoutes)
   
    root.geometry("600x600")
    root.mainloop()
    
    