#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Overall Model for the linear program.

"""

import pulp
import time


class SPDModel(object):
    """SPDModel

    Container for setting up, solving, and organising the results
    of a Simulation. Contains three primary API methods.
    Creation of the Linear Program, solving the LP and parsing the results.

    Usage:
    ------
    solver = SPDModel(SystemOperator)
    solver.create_lp()
    solver.solve_lp()
    solver.parse_result()

    """
    def __init__(self, ISO):
        super(SPDModel, self).__init__()

        self.ISO = ISO

    def create_lp(self):
        """ Publically exposed API
        Creates the Linear program including applying the objective
        function and adding all of the necessary constraints.
        This exists as a wrapper around a number of hidden functions.

        """
        self._setup_lp()
        self._create_variables()
        self._obj_function()
        self._nodal_demand()
        self._energy_offers()
        self._reserve_offers()
        self._transmission_offer()
        self._reserve_proportion()
        self._reserve_combined()
        self._generator_risk()
        self._transmission_risk()
        self._reserve_dispatch()

    def write_lp(self, fName=None):
        """ Write the Linear Program to a file """
        self.lp.writeLP(fName)

    def solve_lp(self):
        """ Solve the Linear Program including the time taken to solve it """
        begin = time.time()
        self.lp.solve()
        self.solution_time = time.time() - begin

    def parse_result(self):
        """ Publically exposed API
        Parse the Results of the solved Linear Program.
        Must be called after solving it.

        """
        self._parse_risk()
        self._parse_energy_prices()
        self._parse_reserve_prices()
        self._parse_branch_flow()
        self._parse_reserve_dispatch()
        self._parse_energy_dispatch()

    def _setup_lp(self):
        """ Setup a Linear Program from a defined ISO instance
        Contains several convenience mappings to shorten line lengths

        """

        # Set up a Linear Program

        self.lp = pulp.LpProblem("SPD Dispatch", pulp.LpMinimize)

        self.addC = self.lp.addConstraint
        self.SUM = pulp.lpSum
        self.lpDict = pulp.LpVariable.dicts

        return self

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

    def _obj_function(self):
        """ Objective Function

        min \sum_i p_{g,i}g_{i} + \sum_j p_{r,j}r_{j}
        """

        # Unpack the necessary variables
        eoffers = self.energy_offers
        eprices = self.ISO.energy_station_price
        roffers = self.reserve_offers
        rprices = self.ISO.reserve_station_price
        enames = self.ISO.energy_station_names
        rnames = self.ISO.reserve_station_names

        # Set the objective function
        self.lp.setObjective(self.SUM(
                             [eoffers[i] * eprices[i] for i in enames]) +
                             self.SUM([roffers[j] * rprices[j]
                                       for j in rnames]))

    def _nodal_demand(self):
        """ Nodal Demand constraints

        Injection_{n} = \sum_{j} g_{j(n)} - d_{n}

        Injection_{n} = \sum_{t} f_{t(n)} * d_{t(n)}

        """
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
            self.addC(node_inj[node] == self.SUM([energy_offer[i]
                                                 for i in nodal_stations[node]]
                                                 ) - nodal_demand[node], n1)

            # Net Injection from transmission
            self.addC(node_inj[node] == self.SUM([branch_flow[t] * flow_dir[t]
                                                 for t in flow_map[node]]), n2)

    def _energy_offers(self):
        """Energy offer constraints

        g_{i} \le g_{max, i}

        """
        # Unpack variables
        eoffers = self.energy_offers
        enames = self.ISO.energy_station_names
        ecapacity = self.ISO.energy_station_capacity

        for i in enames:
            name = '_'.join([i, 'Total_Energy'])
            self.addC(eoffers[i] <= ecapacity[i], name)

    def _reserve_offers(self):
        """ Reserve Offer constraints

        r_{j} \le r_{max, j}

        """
        # Unpack variables
        roffers = self.reserve_offers
        rnames = self.ISO.reserve_station_names
        rcapacity = self.ISO.reserve_station_capacity

        for i in rnames:
            name = '_'.join([i, "Total_Reserve"])
            self.addC(roffers[i] <= rcapacity[i], name)

    def _transmission_offer(self):
        """ Transmission Offer constraints

        f_{t} \le f_{max, t}

        f_{t} \ge -f_{max, t}

        """

        bflows = self.branch_flow
        bnames = self.ISO.branch_names
        bcapacity = self.ISO.branch_capacity

        for i in bnames:
            n1 = '_'.join([i, 'Pos_flow'])
            n2 = '_'.join([i, 'Neg_flow'])

            self.addC(bflows[i] <= bcapacity[i], n1)
            self.addC(bflows[i] >= bcapacity[i] * -1, n2)

    def _reserve_proportion(self):
        """ Reserve Proportion Constraints

        r_{i} \le k_{i}g_{i}

        """

        # Unpack Variables

        spin_stations = self.ISO.reserve_spinning_stations
        roffers = self.reserve_offers
        eoffers = self.energy_offers
        rprop = self.ISO.reserve_station_proportion

        for i in spin_stations:
            name = '_'.join([i, 'Reserve_Proportion'])
            self.addC(roffers[i] <= rprop[i] * eoffers[i], name)

    def _reserve_combined(self):
        """ Reserve total capacity constraints

        r_{i} + g_{i} \le g_{capacity, i}

        """
        spin_stations = self.ISO.reserve_spinning_stations
        roffers = self.reserve_offers
        eoffers = self.energy_offers
        tot_capacity = self.ISO.total_station_capacity

        for i in spin_stations:
            name = '_'.join([i, 'Total_Capacity'])
            self.addC(roffers[i] + eoffers[i] <= tot_capacity[i], name)

    def _generator_risk(self):
        """ Risk for generators

        Risk_{r} \ge g_{i(r)}

        """

        rzones = self.ISO.reserve_zone_names
        rzone_risk = self.reserve_zone_risk

        rzone_stations = self.ISO.reserve_zone_generators
        eoffers = self.energy_offers

        for i in rzones:
            for j in rzone_stations[i]:
                name = '_'.join([i, j, 'Generator_Risk'])
                self.addC(rzone_risk[i] >= eoffers[j], name)

    def _transmission_risk(self):
        """ Risk for a Transmission line

        Risk_{r} \ge f_{t(r)} * d_{t(r)}

        """

        rzones = self.ISO.reserve_zone_names
        rzone_risk = self.reserve_zone_risk

        bflow = self.branch_flow
        bflow_dir = self.ISO.reserve_zone_flow_direction
        bflow_map = self.ISO.reserve_zone_flow_map

        for i in rzones:
            for j in bflow_map[i]:
                name = '_'.join([i, j, "Transmission_Risk"])
                self.addC(rzone_risk[i] >= bflow[j] * bflow_dir[j], name)

    def _reserve_dispatch(self):
        """ Total Reserve Dispatch

        \sum_{j(r)} r_{j} \ge Risk_{r}

        """

        rzones = self.ISO.reserve_zone_names
        rzone_risk = self.reserve_zone_risk

        rzone_stations = self.ISO.reserve_zone_reserve
        roffer = self.reserve_offers

        for i in rzones:
            name = '_'.join([i, 'Reserve_Price'])
            self.addC(self.SUM([roffer[j]
                               for j in rzone_stations[i]]
                               ) >= rzone_risk[i], name)

    def _parse_energy_prices(self):
        """ Parse The Energy Prices """
        self.final_energy_prices = self._condict("Energy_Price")

    def _parse_reserve_prices(self):
        """ Parse the Reserve Prices """
        self.final_reserve_prices = self._condict("Reserve_Price")

    def _parse_energy_dispatch(self):
        """ Parse the Energy Dispatch """
        self.final_energy_dispatch = self._vardict("Energy_Total")

    def _parse_reserve_dispatch(self):
        """ Parse the Reserve Dispatch """
        self.final_reserve_dispatch = self._vardict('Reserve_Total')

    def _parse_branch_flow(self):
        """ Parse the Branch Flows """
        self.final_branch_flow = self._vardict('Transmission_Total')

    def _parse_risk(self):
        """ Parse the Risk parameters """
        self.final_risk_requirements = self._vardict("Reserve_Risk")

    def _vardict(self, condition):
        """ Generic method for extracting values from variables """
        return {n: n.varValue for n in self.lp.variables()
                if condition in n.name}

    def _condict(self, condition):
        """ Generic method for extracting values from constraints """
        return {n: self.lp.constraints[n].pi
                for n in self.lp.constraints if condition in n}

if __name__ == '__main__':
    pass
