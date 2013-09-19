#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pulp
import time
from collections import defaultdict

# C Libraries
import pandas as pd

class Analytics(object):
    """docstring for Analytics"""
    def __init__(self, SPD):
        super(Analytics, self).__init__()
        self.lp = SPD.lp
        self.ISO = SPD.ISO
        SPD.ISO.Analysis = self
        self._parse_result()
        self.create_price_df()
        self.create_dispatch_df()
        self.create_reserve_df()
        self.create_flow_df()
        self.create_master()

    def revenue_calculations(self, stations, interruptible_loads):
        """

        """

        self.station_revenue = pd.concat(self._station_revenue(stations),
                                         axis=1)
        self.interruptible_load_revenue = pd.concat(
                    self._interruptible_load_revenue(interruptible_loads),
                    axis=1)

        self.all_revenue = pd.concat((self.station_revenue,
                                     self.interruptible_load_revenue), axis=1)


    def _interruptible_load_revenue(self, interruptible_loads):
        """ Generator to make the interruptible load revenue calculations"""
        for load in interruptible_loads:
            name, zone = (load.name, load.node.RZ.name)

            load.reserve_dispatch = self.master[' '.join([name, 'Reserve Total'])]
            load.reserve_price = self.master[' '.join([zone, "Reserve Price"])]
            load.reserve_revenue = load.reserve_dispatch * load.reserve_price
            load.reserve_revenue.name = " ".join([name, "Reserve Revenue"])
            yield load.reserve_revenue

    def _station_revenue(self, stations):
        """ Generator to make the station revenue calculations`
        """
        for station in stations:
            name, node, zone = (station.name, station.node.name,
                                station.node.RZ.name)

            station.energy_dispatch = self.master[' '.join([name, 'Energy Total'])].copy()
            station.energy_price  = self.master[' '.join([node, "Energy Price"])].copy()
            station.reserve_dispatch = self.master[' '.join([name,
                                                             'Reserve Total'])
                                                  ].copy()
            station.reserve_price = self.master[' '.join([zone,
                                                         "Reserve Price"]
                                                         )].copy()

            # Cost Calculations
            station.energy_cost = station.energy_dispatch.apply(station.energy_cost_func)
            station.energy_cost.name = "Energy Cost"
            station.reserve_cost = station.reserve_dispatch.apply(station.reserve_cost_func)
            station.reserve_cost.name = "Reserve Cost"

            # Revenue Calculations
            station.energy_revenue = station.energy_dispatch * station.energy_price
            station.energy_revenue.name = " ".join([name, "Energy Revenue"])
            station.reserve_revenue = station.reserve_dispatch * station.reserve_price
            station.reserve_revenue.name = " ".join([name, "Reserve Revenue"])
            station.total_revenue = station.energy_revenue + station.reserve_revenue
            station.total_revenue.name = " ".join([name, "Total Revenue"])

            # Profit Calculations
            station.energy_profit = station.energy_revenue - station.energy_cost
            station.energy_profit.name = "Energy Profit"
            station.reserve_profit = station.reserve_revenue - station.reserve_cost
            station.reserve_profit.name = "Reserve Profit"
            station.total_profit = station.total_revenue - station.energy_cost - station.reserve_cost
            station.total_profit.name = "Total Profit"

            # Yield The Revenue
            yield pd.concat((station.energy_revenue,
                             station.reserve_revenue,
                             station.total_revenue), axis=1)


    def create_master(self):
        """ Create a DataFrame containing information about
        the entire system

        """

        prices = self._parse_to_df([self.final_energy_prices,
                                    self.final_reserve_prices],
                                    parse_type="Constraint")
        dispatch = self._parse_to_df([self.final_energy_dispatch,
                                      self.final_reserve_dispatch],
                                      parse_type="Variable")
        risk = self._parse_to_df([self.final_risk_requirements],
                                 parse_type="Variable")
        flows = self._parse_to_df([self.final_branch_flow],
                                  parse_type="Variable")

        self.master = pd.concat([prices, dispatch, flows, risk], axis=1)

    def create_flow_df(self):
        """ Create a DataFrame of Transmission Flows

        """

        self.branch_flows = self._parse_to_df([self.final_branch_flow], parse_type="Variable")

    def create_reserve_df(self):
        """ Create a DataFrame of Reserve prices and requirements

        """

        prices = self._parse_to_df([self.final_reserve_prices],
                                    parse_type="Constraint")
        requirement = self._parse_to_df([self.final_risk_requirements],
                                         parse_type="Variable")

        self.reserve_df = pd.concat([prices, requirement], axis=1)

    def create_dispatch_df(self):
        """ Create a DataFrame of Energy and Reserve Dispatches
        Based upon the solution to the dispatch and different instances
        passed.

        Parameters
        ----------
        self.final_energy_dispatch: dict
            Dictionary of the final energy dispatches
        self.final_reserve_dispatch: dict
            Dictionary of the final reserve dispatches

        Returns
        -------
        self.final_dispatch_df: DataFrame
            DataFrame of the final energy and reserve dispatches for the
            different units

        """
        self.final_dispatch_df = self._parse_to_df([self.final_energy_dispatch,
                                                 self.final_reserve_dispatch],
                                                 parse_type="Variable")

    def create_price_df(self):
        """ Create a DataFrame of Energy and Reserve Prices
        Based upon the solution to the dispatch and the different
        instances passed. Apply an index to sort by the changing variable
        in question.

        Parameters
        ----------
        self.final_energy_prices: dict
            Dictionary of the final energy prices
        self.final_reserve_prices: dict
            Dictionary of the final reserve prices

        Returns
        -------
        self.final_price_df: DataFrame
            DataFrame of the final energy and reserve prices sorted by
            the actor variable as the index

        """

        self.final_price_df = self._parse_to_df([self.final_energy_prices,
                                                 self.final_reserve_prices],
                                                 parse_type="Constraint")

    def _parse_to_df(self, dicts, parse_type="Constraint"):
        """ Parse one or more dictionary objects (contained in a list)
        to a DataFrame. Will iterate through the objects to create
        one large dictionary, and then parse that to a dict of dicts
        which are then used to create the DataFrame.

        Parameters
        ----------
        dicts: list, iterable
            List of dictionaries to be parsed
        parse_type: string, "Constraint" or "Variable"
            Whether to use the constraint or variable parser

        Returns
        -------
        df: DataFrame
        """

        if len(dicts) >= 2:
            pairings, rest = dicts[0].copy(), dicts[1:]
            for d in rest:
                pairings.update(d)
        else:
            pairings = dicts[0].copy()

        sample_dict = defaultdict(dict)

        for key, value in pairings.iteritems():
            if parse_type == "Constraint":
                keydict = self._parse_constraint_key(key)
            else:
                keydict = self._parse_variable_key(key.name)

            ind_key = ' '.join([keydict['iter-actor'],
                                keydict['iter-actor-var'].title()])
            name = ' '.join([keydict['result-actor'], keydict['variable']])
            sample_dict[name][keydict['var-value']] = int(value)

        df = pd.DataFrame(sample_dict)
        df.index.name = ind_key
        df.index = df.index.astype(int)
        df.sort_index(inplace=True)

        return df

    def _parse_variable_key(self, key):
        """ Function to Parse the key and return the result as a dictionary
        for indexing.
        """

        tup = key.split('_')
        keydict = {'iter-actor': tup[2],
                   'iter-actor-var': ' '.join(tup[3:5]),
                   'var-value': tup[5],
                   'result-actor': "_".join(tup[6:]),
                   'variable': ' '.join(tup[:2])
                    }
        return keydict


    def _parse_constraint_key(self, key):
        """ Function to Parse the key and return the result as a dictionary
        for indexing.
        """

        tup = key.split('_')
        keydict = {'iter-actor': tup[0],
                   'iter-actor-var': ' '.join(tup[1:3]),
                   'var-value': tup[3],
                   'result-actor': tup[4],
                   'variable': ' '.join(tup[-2:])
                    }
        return keydict

    def _parse_result(self):
        """ Parse the Results of the solved Linear Program.
        Must be called after solving it.

        """
        self._parse_risk()
        self._parse_energy_prices()
        self._parse_reserve_prices()
        self._parse_branch_flow()
        self._parse_reserve_dispatch()
        self._parse_energy_dispatch()

    def _parse_energy_prices(self):
        """ Parse The Energy Prices """
        neg_prices = self._condict("Energy_Price")
        self.final_energy_prices = {k: v*-1 for k, v in neg_prices.iteritems()}

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
