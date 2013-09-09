#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# SYSTEM OPERATOR
# ----------------------------------------------------------------------------

class SystemOperator(object):
    """System Operator class takes all of the """
    def __init__(self):
        super(SystemOperator, self).__init__()
        self._create_empty_variables()

    def _create_empty_variables(self):
        self.stations = []
        self.station_names = []
        self.station_map = {}

        self.nodes = []
        self.node_names = []
        self.node_map = {}

        self.reserve_zones = []
        self.reserve_zone_names = []
        self.reserve_zone_map = {}

        self.interruptible_loads = []
        self.interruptible_load_names = []
        self.interruptible_load_map = {}

        self.branches = []
        self.branch_names = []
        self.branch_map = {}

    def _add_station(self, Station):
        """ Add a Station """
        self.stations.append(Station)
        self.station_names.append(Station)
        self.station_map[Station.name] = Station

    def _add_node(self, Node):
        self.nodes.append(Node)
        self.node_names.append(Node.name)
        self.node_map[Node.name] = Node

    def _add_reserve_zone(self, RZ):
        self.reserve_zones.append(RZ)
        self.reserve_zone_names.append(RZ.name)
        self.reserve_zone_map[RZ.name] = RZ

    def _add_interruptible_load(self, IL):
        self.interruptible_loads.append(IL)
        self.interruptible_load_names.append(IL.name)
        self.interruptible_load_map[IL.name] = IL

    def _add_branch(self, Branch):
        self.branches.append(Branch)
        self.branch_names.append(Branch.name)
        self.branch_map[Branch.name] = Branch

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

