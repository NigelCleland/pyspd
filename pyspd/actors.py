#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Library Imports

# C Imports
import numpy as np
from collections import defaultdict

# ----------------------------------------------------------------------------
# SYSTEM OPERATOR
# ----------------------------------------------------------------------------

class SystemOperator(object):
    """System Operator class takes all of the """
    def __init__(self):
        super(SystemOperator, self).__init__()
        self._create_empty_variables()


    def create_iterator(self, actor=None, variable='reserve_price', varrange=np.arange(0,5)):
        """ Take the actor and update all of the variable names

        """

        self.itinstances = []
        self.itdispatches = {}

        if variable
            for value in varrange:
                itname = ''.join([variable, str(value)])
                self.itinstances.apend(itname)
                actor.__dict__[variable] = value
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
        pass

    def _station_parameters(self, itname):
        for station in self.stations:
            name = '_'.join([itname, station.name])
            self.energy_station_names.append(name)
            self.energy_station_capacity[name] = station.energy_offer
            self.energy_station_price[name] = station.energy_price

            self.reserve_station_names.append(name)
            self.reserve_station_capacity[name] = station.reserve_offer
            self.reserve_station_price[name] = station.reserve_price
            self.reserve_station_proportion[name] = station.reserve_proportion



    def _interruptible_load_parameters(self, itname):
        for IL in self.interruptible_loads:
            name = '_'.join([itname, IL.name])
            self.reserve_IL_names.append(name)
            self.reserve_IL_capacity[name] = IL.reserve_offer
            self.reserve_IL_price[name] = IL.reserve_price


    def _node_parameters(self, itname):
        for node in self.nodes:
            name = '_'.join([itname, node.name])
            self.node_names.append(name)
            self.nodal_demand[name] = node.demand

            # Nodal Stations
            for station in node.stations:
                stat_name = '_'.join([itname, station.name])
                self.nodal_stations[name].append(stat_name)


    def _transmission_parameters(self, itname):
        for branch in self.branches:
            name = '_'.join([itname, branch.name])
            sn_name = '_'.join([itname, branch.sending_node.name])
            rn_name = '_'.join([itname, branch.receiving_node.name])

            self.branch_names.append(name)

            self.node_flow_map[sn_name].append(name)
            self.node_flow_map[rn_name].append(name)

            self.node_flow_direction[sn_name][name] = 1
            self.node_flow_direction[rn_name][name] = -1

            if branch.risk:
                sn_rz_name = '_'.join([itname, branch.sending_node.RZ.name])
                rn_rz_name = '_'.join([itname, branch.receiving_node.RZ.name])

                if sn_rz_name != rn_rz_name:

                    self.reserve_zone_flow_map[sn_rz_name].append(name)
                    self.reserve_zone_flow_map[rn_rz_name].append(name)

                    self.reserve_zone_flow_direction[sn_rz_name][name] = 1
                    self.reserve_zone_flow_direction[rn_rz_name][name] = -1


    def _rezerve_zone_parameters(self, itname):
        for rz in self.reserve_zones:
            name = '_'.join([itname, rz.name])

            self.reserve_zone_names.append(name)

            for station in rz.stations:
                stat_name = '_'.join([itname, station.name])
                self.reserve_zone_reserve[name].append(stat_name)
                self.reserve_zone_generators[name].append(stat_name)

            for il in rz.interruptible_loads:
                il_name = '_'.join([itname, il.name])
                self.reserve_zone_reserve[name].append(il_name)



    def _create_empty_variables(self):
        self.stations = []
        self.station_names = []
        self.station_map = {}

        self.energy_station_names = []
        self.reserve_station_names = []
        self.energy_station_price = {}
        self.energy_station_capacity = {}
        self.reserve_station_price = {}
        self.reserve_station_proportion = {}
        self.reserve_station_capacity = {}

        self.nodes = []
        self.node_names = []
        self.node_map = {}
        self.node_flow_direction = defaultdict(dict)
        self.node_flow_map = defaultdict(list)
        self.nodal_stations = defaultdict(list)
        self.nodal_demand = {}

        self.reserve_zones = []
        self.reserve_zone_names = []
        self.reserve_zone_generators = defaultdict(list)
        self.reserve_zone_reserve = defaultdict(list)
        self.reserve_zone_transmission = defaultdict(list)
        self.reserve_zone_flow_map = defaultdict(list)
        self.reserve_zone_flow_direction = defaultdict(dict)

        self.interruptible_loads = []
        self.interruptible_load_names = []
        self.interruptible_load_map = {}

        self.reserve_IL_names = []
        self.reserve_IL_capacity = {}
        self.reserve_IL_price = {}

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

    def _add_interruptible_load(self, IL):
        self.interruptible_loads.append(IL)
        return self


class Node(object):
    """docstring for Node"""
    def __init__(self, name, SO, RZ, demand=0):
        super(Node, self).__init__()
        self.name = name
        self.demand = demand

        self.stations = []
        self.interruptible_loads = []

        RZ._add_node(self)
        self.RZ = RZ

        SO._add_node(self)
        self.SO = SO



    def _add_station(self, Station):
        self.stations.append(Station)
        self.RZ._add_station(Station)
        return self

    def _add_interruptible_load(self, IL):
        self.interruptible_loads.append(IL)
        self.RZ._add_intload(IL)
        return self


class ReserveZone(object):
    """docstring for ReserveZone"""
    def __init__(self, name, SO):
        super(ReserveZone, self).__init__()
        self.name = name
        self.nodes = []

        self.stations = []
        self.interruptible_loads = []

        self.SO = SO
        SO._add_reserve_zone(self)


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
    def __init__(self, name, SO, Node, Company, capacity=0):
        super(Station, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company
        self.capacity = capacity

        Node._add_station(self)
        Company._add_station(self)

        self.SO = SO
        SO._add_station(self)



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
    def __init__(self, name, SO, Node, Company):
        super(InterruptibleLoad, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company

        Node._add_interruptible_load(self)
        Company._add_interruptible_load(self)

        SO._add_interruptible_load(self)


    def add_reserve_offer(self, price, offer):

        self.reserve_price = price
        self.reserve_offer = offer
        return self


class Branch(object):
    """docstring for Branch"""
    def __init__(self, SO, sending_node, receiving_node, capacity=0, risk=False):
        super(Branch, self).__init__()

        SO._add_branch(self)

        # Add the nodes
        self.sending_node = sending_node
        self.receiving_node = receiving_node

        self.capacity = capacity

        self.name = '_'.join([sending_node.name, receiving_node.name])

        self.risk = risk



def test_options():

    operator = SystemOperator()
    RZ = ReserveZone('RZ', operator)
    company = Company('company')
    node = Node("node", operator, RZ, demand=154)

    station = Station('station', operator, node, company, capacity=300)
    il = InterruptibleLoad('il', operator, node, company)

    station.add_reserve_offer(50,300, 0.5)
    station.add_energy_offer(25, 250)

    il.add_reserve_offer(75, 50)

    return (operator, RZ, company, node, station, il)





if __name__ == '__main__':
    pass

