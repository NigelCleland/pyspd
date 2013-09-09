#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Overall Model for the linear program.

"""

import pulp


class SPDModel(object):
    """docstring for SPDModel"""
    def __init__(self):
        super(SPDModel, self).__init__()


    def setup_lp(self):
        """ Setup a Linear Program from a defined ISO instance """

        # Set up a Linear Program

        self.lp = pulp.LpProblem("SPD Dispatch", pulp.LpMinimize)

        self.addC = self.lp.addConstraint
        self.SUM = lp.lpSum
        self.lpDict = pulp.LpVariable.dicts

        return self




