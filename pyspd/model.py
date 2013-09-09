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

        for itname in self.ISO.itinstances:

            # Apply the Constraints for each instance
            pass

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

