===============================
pyspd
===============================

.. image:: https://badge.fury.io/py/pyspd.png
    :target: http://badge.fury.io/py/pyspd

.. image:: https://travis-ci.org/NigelCleland/pyspd.png?branch=master
        :target: https://travis-ci.org/NigelCleland/pyspd

.. image:: https://pypip.in/d/pyspd/badge.png
        :target: https://crate.io/packages/pyspd?version=latest


Simplified version of SPD for analysis

* Free software: BSD license
* Documentation: http://pyspd.rtfd.org.

Features
--------

This module implements a high level method of interacting with a grid
dispatch modelled upon the NZ method. It does not implement a 1:1
representation of the model. Instead it is a framework which is capable of
handling the following:

* Multiple Nodes
* Multiple Stations
* Generation and Energy from Stations
* Reserve only Interruptible Load
* Multiple Transmission Branches
* Multiple Reserve Zones
* Generator and Transmission Risk Setters
* Nodal Marginal Energy Pricing
* Zonal Marginal Reserve Pricing
* Multiple Trading Companies
* Automated Revenue and Dispatch calculations
* Vectorised implementation to take into account a sensitivity analysis
through a simple interface

It accomplishes this by providing an interface for creating entities with
offers which are compiled together. Broadly the user defines a state, e.g. a
Station and then adds offers to this.
The user should not have to have any knowledge of linear programming in
order to use the model.

Usage
-----

```
from pyspd import *

# Define an Operator
operator = SystemOperator()

# Define Reserve Zones
RZ1 = ReserveZone("RZ1", operator)

# Define a Node
Node1 = Node("Node1", operator, RZ1, demand=150)
Node2 = Node("Node2", operator, RZ1, demand=150)

# Define a Branch
Line = Branch(operator, Node1, Node2, capacity=500, risk=False)

# Define a Company
Profiteer = Company("Profiteer")
Market = Company("Market")

# Define Stations
StationOne = Station("StationOne", operator, Node1, Profiteer, capacity=500)
StationTwo = Station("StationTwo", operator, Node2, Market, capacity=500)

# Add Energy and Reserve Offers
StationOne.add_energy_offer(25, 300)
StationOne.add_reserve_offer(25, 300, 1)

StationTwo.add_energy_offer(50,500)
StationTwo.add_reserve_offer(75,400, 1)

# Create an Iterator to vary an offer
operator.create_iterator(StationOne, "energy_price", [10,20,30,40,50])

# Set up the Solver and Solve the model
lpsolver = SPDModel(operator)
lpsolver.full_run()

# Run the Analytics
results = Analytics(lpsolver.lp)
```
