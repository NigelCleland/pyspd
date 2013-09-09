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
        self.SUM = lp.lpSum
        self.lpDict = pulp.LpVariable.dicts

        return self

    def create_lp(self):

        # Create the objective function

        # Iterate over the difference instances:

        pass

    def _create_variables(self):
        """ Create all of the variables necessary to solve the Linear Program
        This maps the variables from the ISO to the requisite Linear Program
        Variables

        Returns:
        --------
        energy_band_offers:
        reserve_band_offers
        transmission_band_offers
        energy_total_offers
        reserve_total_offers
        transmission_total_offers
        nodal_injection
        reserve_zone_risk
        """


        self.energy_band_offers = self.lpDict("Energy_Band",
                        self.ISO.energy_band_offers, 0)

        self.reserve_band_offers = self.lpDict("Reserve_Band",
                        self.ISO.reserve_band_offers, 0)

        self.transmission_band_offers = self.lpDict("Transmission_Band",
                        self.ISO.transmission_band_offers)

        self.energy_total_offers = self.lpDict("Energy_Total",
                        self.ISO.energy_total_offers, 0)

        self.reserve_total_offers = self.lpDict("Reserve_Total",
                        self.ISO.reserve_total_offers, 0)

        self.transmission_total_offers = self.lpDict("Transmission_Total",
                        self.ISO.transmission_total_offers)

        self.nodal_injection = self.lpDict("Nodal_Injection",
                        self.ISO.nodal_injection)

        self.reserve_zone_risk = self.lpDict("Reserve_Risk",
                        self.ISO.reserve_zone_risk, 0)


    def _nodal_demand(self):
        """ Apply the nodal demand constraints """
        pass

    def _obj_function(self):
        """ Apply the objective function """
        pass

    def _energy_band_offers(self):
        pass

    def _reserve_band_offers(self):
        pass

    def _transmission_band_capacity(self):
        pass

    def _energy_total_offers(self):
        pass

    def _reserve_total_offers(self):
        pass

    def _transmission_total_offer(self):
        pass

    def _reserve_proportion(self):
        pass

    def _reserve_combined(self):
        pass

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

