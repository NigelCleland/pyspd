#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# SYSTEM OPERATOR
# ----------------------------------------------------------------------------

class SystemOperator(object):
    """System Operator class takes all of the """
    def __init__(self):
        super(SystemOperator, self).__init__()

        self.stations = []
        self.nodes = []
        self.reserve_zones = []
        self.interruptible_loads = []
        self.branches = []

    def _add_station(self, Station):
        """ Add a Station """
        self.stations.append(Station)

    def _add_node(self, Node):
        self.nodes.append(Node)

    def _add_reserve_zone(self, RZ):
        self.reserve_zones.append(RZ)

    def _add_interruptible_load(self, IL):
        self.interruptible_loads.append(IL)

    def _add_branch(self, Branch):
        self.branches.append(Branch)

# Define an Operator Class each time this is run!
# This is a little bit of magic to make sure the decorators work
# Automatically creates the operator class for the user
# Do not change the ordering here!
operator = SystemOperator()

# ----------------------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------------------

def addStation(cls):
    def wrapped(cls, *args, **kargs):
        operator._add_station(cls)
    return wrapped

def addNode(cls):
    def wrapped(cls, *args, **kargs):
        operator._add_node(cls)
    return wrapped

def addRZ(cls):
    def wrapped(cls, *args, **kargs):
        operator._add_reserve_zone(cls)
    return wrapped

def addIL(cls):
    def wrapped(cls, *args, **kargs):
        operator._add_interruptible_load(cls)
    return wrapped

def addBranch(cls):
    def wrapped(cls, *args, **kargs):
        operator.add_branch(cls)
    return wrapped


# ----------------------------------------------------------------------------
# PARTICIPANT CLASSES
# ----------------------------------------------------------------------------


class Company(object):
    """docstring for Company"""
    def __init__(self, name):
        super(Company, self).__init__()
        self.name = name


class Node(object):
    """docstring for Node"""
    @addNode
    def __init__(self, name, RZ, demand=0):
        super(Node, self).__init__()
        self.name = name
        self.demand = demand

        self.stations = []
        self.intload = []

        RZ._add_node(self)

    def _add_station(self, Station):
        self.stations.append(Station)

    def _add_intload(self, IL):
        self.intload.append(IL)


class ReserveZone(object):
    """docstring for ReserveZone"""
    @addRZ
    def __init__(self, name):
        super(ReserveZone, self).__init__()
        self.name = name
        self.nodes = []


    def _add_node(self, Node):
        self.nodes.append(Node)


class Station(object):
    """docstring for Station"""

    @addStation
    def __init__(self, name, Node):
        super(Station, self).__init__()
        self.name = name

        Node._add_station(self)


class InterruptibleLoad(object):
    """docstring for InterruptibleLoad"""
    @addIL
    def __init__(self, name):
        super(InterruptibleLoad, self).__init__()
        self.name = name

class Branch(object):
    """docstring for Branch"""
    @addBranch
    def __init__(self, sending_node, receiving_node):
        super(Branch, self).__init__()



if __name__ == '__main__':
    pass

