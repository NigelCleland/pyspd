#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Library Imports
from collections import defaultdict

# C Imports
import numpy as np
import pandas as pd
# ----------------------------------------------------------------------------
# SYSTEM OPERATOR
# ----------------------------------------------------------------------------


class SystemOperator(object):
    """System Operator

    This is a container which contains all of the information about the
    System. This includes demand data, nodes, stations etc.
    It must be created first when developing a simulation.

    Once it has been created it is passed to the creation of any other
    object upon which it will automatically update itself.

    Once the simulation has been fully defined it is passed to the
    SPDmodel instance which draws all of the necessary variables
    and values. These are taken and a Linear Program created which
    is solved.

    Usage:
    ------
    operator = SystemOperator()

    """
    def __init__(self):
        super(SystemOperator, self).__init__()
        self._create_empty_variables()

    def create_iterator(self, actor=None, variable='reserve_price',
                        varrange=np.arange(0, 5)):
        """ Create a range of duplicate scenarios which are all solved
        at once to assess the benefits of a particular strategy over
        a particular run.

        This is a user exposed function and must be called whenever a
        run is being created.

        Parameters
        ----------
        actor: Node, Station, InterruptibleLoad
            An object which is to be modified when solving the linear program
        variable: str
            The name of the variable to be modified, e.g. 'reserve_price'
        varrange: iterable
            An iterable of ints or floats which consist of the new values
            for the variable in each instance

        """

        self.itinstances = []
        self.itdispatches = {}

        if actor:
            for value in varrange:
                itname = '_'.join([actor.name, variable, str(value)])
                self.itinstances.append(itname)
                actor.__dict__[variable] = value
                self._add_dispatch(itname)

        else:
            # Do a single dispatch
            itname = "Single"
            self.itinstances.append(itname)

            self._add_dispatch(itname)

        return self

    def _add_dispatch(self, itname):
        """ Convenience wrapper, calls each of the parameter functons
        Acts as a hidden API.

        Parameters
        ----------
        itname: str
            The iterable name to be applied
        """

        self._station_parameters(itname)
        self._interruptible_load_parameters(itname)
        self._node_parameters(itname)
        self._transmission_parameters(itname)
        self._rezerve_zone_parameters(itname)

    def _station_parameters(self, itname):
        """ Hidden function will create a number of lists and dictionaries
        containing information about the Linear Program to be passed
        to the model.

        """
        for station in self.stations:
            name = '_'.join([itname, station.name])
            self.energy_station_names.append(name)
            self.energy_station_capacity[name] = station.energy_offer
            self.energy_station_price[name] = station.energy_price

            self.reserve_station_names.append(name)
            self.reserve_station_capacity[name] = station.reserve_offer
            self.reserve_station_price[name] = station.reserve_price
            self.reserve_station_proportion[name] = station.reserve_proportion

            self.reserve_spinning_stations.append(name)
            self.total_station_capacity[name] = station.capacity

    def _interruptible_load_parameters(self, itname):
        """ Hidden function will create a number of lists and dictionaries
        containing information about the Linear Program to be passed
        to the model.

        """
        for IL in self.interruptible_loads:
            name = '_'.join([itname, IL.name])
            self.reserve_IL_names.append(name)
            self.reserve_IL_capacity[name] = IL.reserve_offer
            self.reserve_IL_price[name] = IL.reserve_price

            self.reserve_station_names.append(name)
            self.reserve_station_price[name] = IL.reserve_price
            self.reserve_station_capacity[name] = IL.reserve_offer

    def _node_parameters(self, itname):
        """ Hidden function will create a number of lists and dictionaries
        containing information about the Linear Program to be passed
        to the model.

        """
        for node in self.nodes:
            name = '_'.join([itname, node.name])
            self.node_names.append(name)
            self.nodal_demand[name] = node.demand

            # Nodal Stations
            for station in node.stations:
                stat_name = '_'.join([itname, station.name])
                self.nodal_stations[name].append(stat_name)

    def _transmission_parameters(self, itname):
        """ Hidden function will create a number of lists and dictionaries
        containing information about the Linear Program to be passed
        to the model.

        """
        for branch in self.branches:
            name = '_'.join([itname, branch.name])
            sn_name = '_'.join([itname, branch.sending_node.name])
            rn_name = '_'.join([itname, branch.receiving_node.name])

            self.branch_names.append(name)

            self.node_flow_map[sn_name].append(name)
            self.node_flow_map[rn_name].append(name)

            self.branch_capacity[name] = branch.capacity

            self.node_flow_direction[sn_name][name] = 1
            self.node_flow_direction[rn_name][name] = -1

            if branch.risk:
                sn_rz_name = '_'.join([itname, branch.sending_node.RZ.name])
                rn_rz_name = '_'.join([itname, branch.receiving_node.RZ.name])

                if sn_rz_name != rn_rz_name:

                    self.reserve_zone_flow_map[sn_rz_name].append(name)
                    self.reserve_zone_flow_map[rn_rz_name].append(name)

                    self.reserve_zone_flow_direction[sn_rz_name][name] = -1
                    self.reserve_zone_flow_direction[rn_rz_name][name] = 1

    def _rezerve_zone_parameters(self, itname):
        """ Hidden function will create a number of lists and dictionaries
        containing information about the Linear Program to be passed
        to the model.

        """
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
        """ Initialises a number of empty lists and dictionaries
        which are used in setting up the linear program

        """
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
        self.total_station_capacity = {}

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
        self.reserve_spinning_stations = []

        self.interruptible_loads = []
        self.interruptible_load_names = []
        self.interruptible_load_map = {}

        self.reserve_IL_names = []
        self.reserve_IL_capacity = {}
        self.reserve_IL_price = {}

        self.branches = []
        self.branch_names = []
        self.branch_map = {}
        self.branch_capacity = {}
        return self

    def _add_station(self, Station):
        """ Adds a station automatically to the System Operator """
        self.stations.append(Station)
        return self

    def _add_node(self, Node):
        """ Adds a node automatically to the System Operator"""
        self.nodes.append(Node)
        return self

    def _add_reserve_zone(self, RZ):
        """ Adds a Reserve Zone automatically to the System Operator """
        self.reserve_zones.append(RZ)
        return self

    def _add_interruptible_load(self, IL):
        """ Adds a Interruptible Load participant to the System Operator """

        self.interruptible_loads.append(IL)
        return self

    def _add_branch(self, Branch):
        """ Adds a Branch to the Systen Operator """
        self.branches.append(Branch)
        return self

# ----------------------------------------------------------------------------
# PARTICIPANT CLASSES
# ----------------------------------------------------------------------------


class Company(object):
    """Company

    A container around a number of Stations and Interruptible Load which
    can be used to determine the aggregate position for a particular company.
    This is useful when determining profits and losses from a particular
    solution ot the model and should speed up the iteration process.
    """
    def __init__(self, name):
        super(Company, self).__init__()
        self.name = name

        self.stations = []
        self.interruptible_loads = []

    def _add_station(self, Station):
        """ Automatically add a station to the Company.
        Is called when a Station is created.

        Parameters
        ----------
        Station: Station
            The station object to be added

        """
        self.stations.append(Station)
        return self

    def _add_interruptible_load(self, IL):
        """ Automatically add an interruptible load to the Company.
        Is called when an interruptible load object is created

        Parameters
        ----------
        IL: InterruptibleLoad
            The interruptible load object to be added

        """
        self.interruptible_loads.append(IL)
        return self

###
# Revenue Calculations
###

    def calculate_profit(self):
        """ Exposed Method

        Wrapper to calculate revenue, costs and profits for all of the
        companies generation stations and interruptible load providers.

        """
        self._company_revenue()
        self._company_cost()
        self._company_profit()

    def _company_profit(self):
        self.unit_profit = pd.concat(self._company_pro, axis=1)
        self.company_profits = self.unit_profit.sum(axis=1)

    def _company_pro(self):
        for station in self.stations:
            yield station.total_profit

        for load in self.interruptible_loads:
            yield load.total_profit

    def _company_revenue(self):
        self.unit_revenue = pd.concat(self._company_rev, axis=1)
        self.company_revenue = self.unit_revenue.sum(axis=1)

    def _company_cost(self):
        self.unit_cost = pd.concat(self._company_costs, axis=1)
        self.company_cost = self.unit_cost.sum(axis=1)

    def _company_rev(self):
        for station in self.stations:
            yield station.total_revenue

        for load in self.interruptible_loads:
            yield load.reserve_revenue

    def _company_costs(self):
        for station in self.stations:
            yield station.total_cost

        for load in self.interruptible_loads:
            yield load.total_cost


class Node(object):
    """Node

    A nodal location within the current system.
    Is part of a reserve zone and acts as a location for demand, generation
    and reserve. Has a number of automatic methods which are called whenever
    a new object is created at the node in question to handle the book
    keeping operations.

    Parameters
    ----------
    name: str
        A unique name for the Node
    SO: SystemOperator
        The system opeartor object
    RZ: ReserveZone
        What reserve zone the node is a part of
    demand: int, float, default 0
        The nodal demand at the node

    """
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
        """ Automatically add a station to both the Node and the Reserve Zone

        Parameters
        ----------
        Station: Station
            The station object to be added

        """
        self.stations.append(Station)
        self.RZ._add_station(Station)
        return self

    def _add_interruptible_load(self, IL):
        """ Automatically add an interruptible load to the Node and
            Reserve Zone.

        Parameters
        ----------
        IL: InterruptibleLoad
            The interruptible load object to be added
        """
        self.interruptible_loads.append(IL)
        self.RZ._add_intload(IL)
        return self


class ReserveZone(object):
    """ReserveZone

    A Reserve Zone is a collection of nodes which have a separate "risk" which
    must be secured against by dispatching reserve from the nodes within the
    zone. Reserve procured from other zones cannot currently be utilised
    to secure a risk in a separate zone

    Parameters
    ----------
    name: str
        Unique name for the Reserve Zone
    SO: SystemOperator
        The System Operator object for the dispatch

    """
    def __init__(self, name, SO):
        super(ReserveZone, self).__init__()
        self.name = name
        self.nodes = []

        self.stations = []
        self.interruptible_loads = []

        self.SO = SO
        SO._add_reserve_zone(self)

    def _add_node(self, Node):
        """ Adds a node automatically to the Reserve Zone.
        Is called automatically whenever a new node is created

        Parameters
        ----------
        Node: Node
            The node to be added to the reserve zone
        """
        self.nodes.append(Node)
        return self

    def _add_station(self, Station):
        """ Adds a station automatically to the Reserve Zone.
        Is called automatically when a new station is created

        Parameters
        ----------
        Station: Station
            The station to be added to the reserve zone

        """
        self.stations.append(Station)
        return self

    def _add_intload(self, IL):
        """ Adds an interruptible load provider to the Rezerve Zone
        Is called automatically when a new station is created

        Parameters
        ----------
        IL: InterruptibleLoad
            The interruptible load object to be added to the reserve zone.

        """
        self.interruptible_loads.append(IL)
        return self


class Station(object):
    """Station

    A generation station for use in the SPD model.
    Is a container around the core functionality that can be called
    automatically by the operator to provide its offers.
    Ideally is a self contained agent that communicates with the SystemOperator

    Parameters
    ----------
    name: str
        Unique name for the Generation Station
    SO: SystemOperator
        Operator object for the situation
    Node: Node
        Location of the generation station
    Company: Company
        Owner of the generation station for determining total revenue etc
    capacity: int, float, default 0
        Total generation capacity of the station

    """

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

        self.energy_cost_func = lambda x: 0
        self.reserve_cost_func = lambda x: 0

    def add_energy_offer(self, price, offer):
        """ Adds an Energy Offer to the station

        Parameters
        ----------
        price: int, float
            The price of the Energy Offer
        offer: int, float
            Offer component of the Energy Offer

        """
        self.energy_price = price
        self.energy_offer = offer
        return self

    def add_reserve_offer(self, price, offer, proportion):
        """ Adds a Reserve Offer to the Station

        Parameters
        ----------
        price: int, float
            The price of the Reserve Offer
        offer: int, float
            Offer component of the Reserve Offer
        proportion: float
            Proportion component of the Reserve Offer

        """
        self.reserve_price = price
        self.reserve_offer = offer
        self.reserve_proportion = proportion
        return self

    def add_energy_cost_func(self, func):

        self.energy_cost_func = func

    def add_reserve_cost_func(self, func):

        self.reserve_cost_func = func

    def calculate_profits(self):
        """ Exposed method to calculate all of a stations energy and
        reserve revenue, costs and profits
        """

        self._energy_revenue()
        self._reserve_revenue()
        self._total_revenue()

        self._energy_cost()
        self._reserve_cost()
        self._total_cost()

        self._energy_profit()
        self._reserve_profit()
        self._total_profit()

    def _energy_revenue(self):
        self.energy_dispatch = self._query(self._name("Energy Total"))
        nd_name = " ".join([self.node.name, "Energy Price"])
        self.energy_price  = self._query(nd_name)
        # Revenue Calculations
        self.energy_revenue = self.energy_dispatch * self.energy_price
        self.energy_revenue.name = self._name("Energy Revenue")

    def _reserve_revenue(self):
        self.reserve_dispatch = self._query(self._name("Reserve Total"))
        rz_name = " ".join([self.node.RZ.name, "Reserve Price"])
        self.reserve_price = self._query(rz_name)

        self.reserve_revenue = self.reserve_dispatch * self.reserve_price
        self.reserve_revenue.name = self._name("Reserve Revenue")

    def _total_revenue(self):
        self.total_revenue = self.energy_revenue + self.reserve_revenue
        self.total_revenue.name = self._name("Total Revenue")

    def _energy_cost(self):
        self.energy_cost = self.energy_dispatch.apply(self.energy_cost_func)
        self.energy_cost.name = self._name("Energy Cost")

    def _reserve_cost(self):
        self.reserve_cost = self.reserve_dispatch.apply(self.reserve_cost_func)
        self.reserve_cost.name = self._name("Reserve Cost")

    def _total_cost(self):
        self.total_cost = self.reserve_cost + self.energy_cost
        self.total_cost.name = self._name("Total Cost")

    def _energy_profit(self):
        self.energy_profit = self.energy_revenue - self.energy_cost
        self.energy_profit.name = self._name("Energy Profit")

    def _reserve_profit(self):
        self.reserve_profit = self.reserve_revenue - self.reserve_cost
        self.reserve_profit.name = self._name("Reserve Profit")

    def _total_profit(self):
        self.total_profit = self.total_revenue - self.total_cost
        self.total_profit.name = self._name("Total Profit")

    def _name(self, adj):
        return " ".join([self.name, adj])

    def _query(self, col):
        """ Note that this is terribly kludgy and I don't like it at all """
        return self.SO.Analysis.master[col].copy()


class InterruptibleLoad(object):
    """InterruptibleLoad

    Container for an Interruptible Load participant within the market.
    This participant acts as a non-generator source of reserve for
    supporting a higher level of risk in the market.

    Currently set up by passing a unique name to the object.

    Parameters
    ----------
    name: str
        The unique name to be applied to the Interruptible Load object
    SO: SystemOperator
        The System Operator object
    Node: Node
        The location of the source of interruptible load
    Company: Company
        Who controls the Interruptible Load object, used when determining
        profits or losses

    """
    def __init__(self, name, SO, Node, Company):
        """ Initialise the interruptible load object"""
        super(InterruptibleLoad, self).__init__()
        self.name = name
        self.node = Node
        self.company = Company
        self.reserve_cost_func = lambda x: 0

        Node._add_interruptible_load(self)
        Company._add_interruptible_load(self)

        SO._add_interruptible_load(self)

    def add_reserve_offer(self, price, offer):
        """ Add a Reserve Offer to the object consisting of a price and offer

        Parameters
        ----------
        price: int, float
            The price of the offer
        offer: int, float
            The quantity of the offer

        """

        self.reserve_price = price
        self.reserve_offer = offer
        return self

    def add_reseve_cost_func(self, func):
        self.reserve_cost_func = func

    def calculate_profits(self):
        """ Exposed method to calculate an interruptible load providers
        profits, costs and revenue
        """
        self._reserve_revenue()
        self._total_revenue()
        self._reserve_cost()
        self._total_cost()
        self._reserve_profit()
        self._total_profit()

    def _reserve_revenue(self):
        self.reserve_dispatch = self._query(self._name("Reserve Total"))
        rz_name = " ".join([self.node.RZ.name, "Reserve Price"])
        self.reserve_price = self._query(rz_name)

        self.reserve_revenue = self.reserve_dispatch * self.reserve_price
        self.reserve_revenue.name = self._name("Reserve Revenue")

    def _total_revenue(self):
        self.total_revenue = self.reserve_revenue.copy()
        self.total_revenue.name = self._name("Total Revenue")

    def _reserve_cost(self):
        self.reserve_cost = self.reserve_dispatch.apply(self.reserve_cost_func)
        self.reserve_cost.name = self._name("Reserve Cost")

    def _total_cost(self):
        self.total_cost = self.reserve_cost.copy()
        self.total_cost.name = self._name("Total Cost")

    def _reserve_profit(self):
        self.reserve_profit = self.reserve_revenue - self.reserve_cost
        self.reserve_profit.name = self._name("Reserve Profit")

    def _total_profit(self):
        self.total_profit = self.total_revenue - self.total_cost
        self.total_profit.name = self._name("Total Profit")

    def _query(self, col):
        """ Note that this is terribly kludgy and I don't like it at all """
        return self.SO.Analysis.master[col].copy()

class Branch(object):
    """Branch

    A Branch is a connection point between any two nodes and specifies
    the capacity between the nodes.
    A branch may be a risk setting object, if the risk flag is set to True
    If this is the case then the current implementation of the model requires
    the sending and receiving node to be in different Reserve Zones.

    To initiate a Branch object a minimum of three items must be passed.

    Parameters
    ----------
    SO: SystemOperator
        The System Operator object for the current solution run
    sending_node: Node
        The node which is specified as the sending node for the model dispatch
    receiving_node: Node
        The receiving node for the model dispatch
    capacity: int, float, default 0
        The capacity of the branch
    risk: bool, default False
        Flag to treat the branch as a risk setting object.

    """
    def __init__(self, SO, sending_node, receiving_node, capacity=0,
                 risk=False):
        super(Branch, self).__init__()

        SO._add_branch(self)

        # Add the nodes
        self.sending_node = sending_node
        self.receiving_node = receiving_node

        self.capacity = capacity

        self.name = '_'.join([sending_node.name, receiving_node.name])

        self.risk = risk

if __name__ == '__main__':
    pass
