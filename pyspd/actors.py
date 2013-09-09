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

operator = SystemOperator()

def addStation(cls):
    def wrapped(cls):
        print operator
        operator.add_station(cls)
        print cls

    return wrapped

class Company(object):
    """docstring for Company"""
    def __init__(self, arg):
        super(Company, self).__init__()

class Node(object):
    """docstring for Node"""
    def __init__(self, arg):
        super(Node, self).__init__()
        self.arg = arg

class ReserveZone(object):
    """docstring for ReserveZone"""
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
    def __init__(self, arg):
        super(InterruptibleLoad, self).__init__()
        self.arg = arg


if __name__ == '__main__':
    pass

