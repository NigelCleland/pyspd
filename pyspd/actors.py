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
        self.itdispatches = {}

        if isinstance(prices, np.ndarray):
            for price in prices:
                itname = ''.join(["Price", str(price)])
                self.itinstances.apend(itname)

                actor.reserve_price = price
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

        return self



    def add_dispatch(self, itname):
        """ Get the dispatch, apply the iterator name to each one
        """

        # Energy Stations
        for station in self.stations:
            name = ' '.join([itname, station.name])
            self.energy_station_names.append(name)
            self.energy_station_capacity[name] = station.energy_offer
            self.energy_station_price[name] = station.energy_price

        # Reserve Stations
        for station in self.stations:
            name = ' '.join([itname, station.name])
            self.reserve_station_names.append(name)
            self.reserve_station_capacity[name] = station.reserve_offer
            self.reserve_station_price[name] = station.reserve_price
            self.reserve_station_proportion[name] = station.proportion

        # Interruptible Load
        for IL in self.interruptible_loads:
            name = ' '.join([itname, IL.name])
            self.reserve_IL_names.append(name)
            self.reserve_IL_capacity[name] = IL.reserve_offer
            self.reserve_IL_price[name] = IL.reserve_price

        # Nodal Demand
        for node in self.nodes:
            name = ' '.join([itname, node.name])
            self.node_names.append(name)
            self.nodal_demand[name] = node.demand

        # Transmisison Branches
        for branch in self.branches:
            pass

        # Reserve Zones
        for rz in self.reserve_zones:
            pass



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
        return self

    def _add_station(self, Station):
        """ Add a Station """
        self.stations.append(Station)
        return self

    def _add_node(self, Node):
        self.nodes.append(Node)
        return self

    def _add_reserve_zone(self, RZ):
        self.reserve_zones.append(RZ)
        return self

    def _add_interruptible_load(self, IL):
        self.interruptible_loads.append(IL)
        return self

    def _add_branch(self, Branch):
        self.branches.append(Branch)
        return self

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
        return self

    def _add_intload(self, IL):
        self.interruptible_loads.append(IL)
        return self


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
        return self

    def _add_intload(self, IL):
        self.intload.append(IL)
        self.RZ._add_intload(IL)
        return self


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
        return self

    def _add_station(self, Station):
        self.stations.append(Station)
        return self

    def _add_intload(self, IL):
        self.interruptible_loads.append(IL)
        return self


class Station(object):
    """docstring for Station"""
    def __init__(self, name, Node, Company, capacity=0):
        super(Station, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company
        self.capacity = capacity

        Node._add_station(self)
        Company._add_station(self)



    def add_energy_offer(self, price, offer):
        self.energy_price = price
        self.energy_offer = offer
        return self


    def add_reserve_offer(self, price, offer, proportion):

        self.reserve_price = price
        self.reserve_offer = offer
        self.reserve_proportion = proportion
        return self


class InterruptibleLoad(object):
    """docstring for InterruptibleLoad"""
    def __init__(self, name, Node, Company):
        super(InterruptibleLoad, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company

        Node._add_intload(self)
        Company._add_intload(self)


    def add_reserve_offer(self, price, offer):

        self.reserve_price = price
        self.reserve_offer = offer
        return self


class Branch(object):
    """docstring for Branch"""
    def __init__(self, sending_node, receiving_node, capacity=0):
        super(Branch, self).__init__()

        # Add the nodes
        self.sending_node = sending_node
        self.receiving_node = receiving_node

        self.capacity = capacity
        # Add the branch to each node




if __name__ == '__main__':
    pass

