#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SystemOperator(object):
    """System Operator class takes all of the """
    def __init__(self):
        super(SystemOperator, self).__init__()

        self.stations = []
        self.nodes = []
        self.reserve_zones = []
        self.interruptible_loads = []

    def add_station(self, Station):
        """ Add a Station """
        self.stations.append(Station)

    def add_node(self, Node):
        self.nodes.append(Node)

    def add_reserve_zone(self, RZ):
        self.reserve_zones.append(RZ)

    def add_interruptible_load(self, IL):
        self.interruptible_loads.append(IL)

# Define an Operator Class each time this is run!
operator = SystemOperator()



def addStation(cls):
    def wrapped(cls, *args, **kargs):
        operator.add_station(cls)
    return wrapped

def addNode(cls):
    def wrapped(cls, *args, **kargs):
        operator.add_node(cls)
    return wrapped

def addRZ(cls):
    def wrapped(cls, *args, **kargs):
        operator.add_reserve_zone(cls)
    return wrapped

def addIL(cls):
    def wrapped(cls, *args, **kargs):
        operator.add_interruptible_load(cls)
    return wrapped


class Company(object):
    """docstring for Company"""
    def __init__(self, arg):
        super(Company, self).__init__()


class Node(object):
    """docstring for Node"""
    @addNode
    def __init__(self, arg):
        super(Node, self).__init__()
        self.arg = arg

class ReserveZone(object):
    """docstring for ReserveZone"""
    @addRZ
    def __init__(self, arg):
        super(ReserveZone, self).__init__()
        self.arg = arg

class Station(object):
    """docstring for Station"""

    @addStation
    def __init__(self):
        super(Station, self).__init__()


class InterruptibleLoad(object):
    """docstring for InterruptibleLoad"""
    @addIL
    def __init__(self, arg):
        super(InterruptibleLoad, self).__init__()
        self.arg = arg


if __name__ == '__main__':
    pass

