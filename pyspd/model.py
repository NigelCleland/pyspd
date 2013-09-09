#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Overall Model for the linear program.

"""

import pulp


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




