from configparser import MAX_INTERPOLATION_DEPTH
from pickle import FALSE, TRUE
import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from functools import partial3

class Bus:
    def _init__(self, num, bus_status, route):
        self.num = num
        self.bus_status = str(bus_status)
class Route:
    def __init__(self, name, num_buses, stops = [], buses = []):
        self.name = str(name)
        self.stops = []
        self.buses = []
        self.num_buses = num_buses
class Stop:
    def __init__(self, campus, num_buses, time2stops = {}):
        self.campus = str(campus)
        self.num_buses = 0
        self.time2stops = {}
#  "AT STOP" , "IN TRANSIT", "TAKING BREAKING"

def readRoutes():
    f = open("BusRoutes.txt", "r")
    lines = f.readlines()
    allRoutes = []

    for x in lines:
        tempLine = x.split(';')
        tempRoute = Route(tempLine[0], )


    return allRoutes

    