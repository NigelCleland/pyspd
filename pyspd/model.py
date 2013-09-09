#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Overall Model for the linear program.

"""

import pulp
import time

class SPDModel(object):
    """docstring for SPDModel"""
    def __init__(self, ISO):
        super(SPDModel, self).__init__()

        self.ISO = ISO

    def setup_lp(self):
        """ Setup a Linear Program from a defined ISO instance """

        # Set up a Linear Program

        self.lp = pulp.LpProblem("SPD Dispatch", pulp.LpMinimize)

        self.addC = self.lp.addConstraint
        self.SUM = pulp.lpSum
        self.lpDict = pulp.LpVariable.dicts

        return self

    def create_lp(self):
        self.setup_lp()
        self._create_variables()
        self._obj_function()
        self._nodal_demand()
        self._energy_offers()

    def _create_variables(self):
        """ Create all of the variables necessary to solve the Linear Program
        This maps the variables from the ISO to the requisite Linear Program
        Variables

        Returns:
        --------
        energy_total_offers
        reserve_total_offers
        branch_flow
        nodal_injection
        reserve_zone_risk
        """


        self.energy_offers = self.lpDict("Energy_Total",
                        self.ISO.energy_station_names, 0)

        self.reserve_offers = self.lpDict("Reserve_Total",
                        self.ISO.reserve_station_names, 0)

        self.branch_flow = self.lpDict("Transmission_Total",
                        self.ISO.branch_names)

        self.nodal_injection = self.lpDict("Nodal_Injection",
                        self.ISO.node_names)

        self.reserve_zone_risk = self.lpDict("Reserve_Risk",
                        self.ISO.reserve_zone_names, 0)


    def _nodal_demand(self):
        """ Apply the nodal demand constraints """
        # Unpack variables

        node_inj = self.nodal_injection
        nodal_demand = self.ISO.nodal_demand
        nodal_stations = self.ISO.nodal_stations
        node_names = self.ISO.node_names

        flow_map = self.ISO.node_flow_map
        flow_dir = self.ISO.node_flow_direction

        energy_offer = self.energy_offers
        branch_flow = self.branch_flow

        for node in node_names:
            n1 = '_'.join([node, 'Energy_Price'])
            n2 = '_'.join([node, 'Nodal_Transmission'])

            # Net Injections from Energy and Demand
            self.addC(node_inj[node] == SUM([energy_offer[i] for i in nodal_stations[node]]) - nodal_demand[node], n1)

            # Net Injection from transmission
            self.addC(node_inj[node] == SUM([branch_flow[t] * flow_dir[t] for t in flow_map[node]]),n2)


    def _obj_function(self):
        """ Apply the objective function """

        # Unpack the necessary variables
        eoffers = self.energy_offers
        eprices = self.ISO.energy_station_price
        roffers = self.reserve_offers
        rprices = self.ISO.reserve_station_price
        enames = self.ISO.energy_station_names
        rnames = self.ISO.reserve_station_names

        # Set the objective function
        self.lp.setObjective(self.SUM(
                [eoffers[i] * eprices[i] for i in enames]) +\
                self.SUM([roffers[j] * rprices[j] for j in rnames]))

    def _energy_offers(self):
        """ Constrain the Energy offers """
        # Unpack variables
        eoffers = self.energy_offers
        enames = self.ISO.energy_station_names
        ecapacity = self.ISO.energy_station_capacity

        for i in enames:
            name = '_'.join([i, 'Total_Energy'])
            self.addC(eoffers[i] <= ecapacity[i], name)


    def _reserve_offers(self):
        # Unpack variables
        roffers = self.reserve_offers
        rnames = self.ISO.reserve_station_names
        rcapacity = self.ISO.reserve_station_capacity

        for i in rnames:
            name = '_'.join([i, "Total_Reserve"])
            self.addC(roffers[i] <= rcapacity[i], name)

    def _transmission_offer(self):
        pass

    def _reserve_proportion(self):

        # Unpack Variables

        spin_stations = self.ISO.reserve_spinning_stations
        roffers = self.reserve_offers
        eoffers = self.energy_offers
        rprop = self.ISO.reserve_station_proportion

        for i in spin_stations:
            name = '_'.join([i, 'Reserve_Proportion'])
            self.addC(roffers[i] <= rprop[i] * eoffers[i], name)

    def _reserve_combined(self):
        spin_stations = self.ISO.reserve_spinning_stations
        roffers = self.reserve_offers
        eoffers = self.energy_offers
        tot_capacity = self.ISO.total_station_capacity

        for i in spin_stations:
            name = '_'.join([i, 'Total_Capacity'])
            self.addC(roffers[i] + eoffers[i] <= tot_capacity[i], name)

    def _generator_risk(self):
        pass

    def _transmission_risk(self):
        pass

    def _reserve_dispatch(self):
        pass

    def write_lp(self, fName=None):
        self.lp.writeLP(fName)

    def solve_lp(self):
        begin = time.time()
        self.lp.solve(pulp.COIN_CMD())
        self.solution_time = time.time() - begin

