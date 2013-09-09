#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Library Imports

# C Imports
import numpy as np

# ----------------------------------------------------------------------------
# SYSTEM OPERATOR
# ----------------------------------------------------------------------------

class SystemOperator(object):
    """System Operator class takes all of the """
    def __init__(self):
        super(SystemOperator, self).__init__()
        self._create_empty_variables()


    def create_iterator(self, actor=None, prices=None, quantities=None):
        """ Take the actor and update all of the variable names

        """

        self.itinstances = []

        if isinstance(prices, np.ndarray):
            for price in prices:
                itname = ''.join(["Price", str(price)])
                self.itinstances.apend(itname)

                actor.add_offer_price(price)
                self.add_dispatch(itname)

        elif isinstance(quantities, np.ndarray):
            for quantity in quantities:
                itname = ''.join(["Quantity", str(quantity)])
                self.itinstances.apend(itname)

                actor.set_offer_quantity(quantity)
                self.add_dispatch(itname)

        else:
            # Do a single dispatch
            itname="Single"
            self.itinstances.apend(itname)

            self.add_dispatch(itname)



    def add_dispatch(self, itname):
        """ Get the dispatch, apply the iterator name to each one
        """



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

# ----------------------------------------------------------------------------
# PARTICIPANT CLASSES
# ----------------------------------------------------------------------------


class Company(object):
    """docstring for Company"""
    def __init__(self, name):
        super(Company, self).__init__()
        self.name = name

        self.stations = []
        self.interruptible_loads = []

    def _add_station(self, Station):
        self.stations.append(Station)

    def _add_intload(self, IL):
        self.interruptible_loads.append(IL)

class Node(object):
    """docstring for Node"""
    def __init__(self, name, RZ, demand=0):
        super(Node, self).__init__()
        self.name = name
        self.demand = demand

        self.stations = []
        self.intload = []

        RZ._add_node(self)
        self.RZ = RZ


    def _add_station(self, Station):
        self.stations.append(Station)
        self.RZ._add_station(Station)

    def _add_intload(self, IL):
        self.intload.append(IL)
        self.RZ._add_intload(IL)


class ReserveZone(object):
    """docstring for ReserveZone"""
    def __init__(self, name):
        super(ReserveZone, self).__init__()
        self.name = name
        self.nodes = []

        self.stations = []
        self.interruptible_loads = []


    def _add_node(self, Node):
        self.nodes.append(Node)

    def _add_station(self, Station):
        self.stations.append(Station)

    def _add_intload(self, IL):
        self.interruptible_loads.append(IL)


class Station(object):
    """docstring for Station"""
    def __init__(self, name, Node, Company):
        super(Station, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company

        Node._add_station(self)
        Company._add_station(self)


class InterruptibleLoad(object):
    """docstring for InterruptibleLoad"""
    def __init__(self, name, Node, Company):
        super(InterruptibleLoad, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company

        Node._add_intload(self)
        Company._add_intload(self)


class Branch(object):
    """docstring for Branch"""
    def __init__(self, sending_node, receiving_node):
        super(Branch, self).__init__()

        # Add the nodes
        self.sending_node = sending_node
        self.receiving_node = receiving_node

        # Add the branch to each node




if __name__ == '__main__':
    pass

