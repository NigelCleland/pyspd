#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyspd
----------------------------------

Tests for `pyspd` module.
"""

import pytest
from pyspd import *

def test_operator_creation():

    operator = SystemOperator()
    assert isinstance(operator, SystemOperator)

def test_rz_creation():

    operator = SystemOperator()

    RZ = ReserveZone("RZ", operator)
    assert RZ.name  == "RZ"
    assert RZ.nodes == []
    assert RZ.stations == []
    assert RZ.interruptible_loads == []

    assert operator.reserve_zones[0] == RZ

def test_node_creation():

    operator = SystemOperator()
    RZ = ReserveZone("RZ", operator)
    node = Node("node", operator, RZ, demand=154)

    assert node.name == 'node'
    assert operator.nodes[0] == node
    assert node.RZ == RZ
    assert RZ.nodes[0] == node
    assert node.demand == 154

def test_company_creation():

    operator = SystemOperator()

    company = Company("company")

    assert company.name == 'company'
    assert company.stations == []
    assert company.interruptible_loads == []

def test_station_creation():

    operator = SystemOperator()
    company = Company("company")
    RZ = ReserveZone("RZ", operator)
    node = Node("node", operator, RZ, demand=154)

    station = Station("station", operator, node, company, capacity=500)

    assert station.name == "station"
    assert station.capacity == 500

    assert operator.stations[0] == station
    assert company.stations[0] == station
    assert node.stations[0] == station
    assert RZ.stations[0] == station

def test_il_creation():

    operator = SystemOperator()
    company = Company("company")
    RZ = ReserveZone("RZ", operator)
    node = Node("node", operator, RZ, demand=154)

    il = InterruptibleLoad('IL', operator, node, company)

    assert il.name == "IL"
    assert operator.interruptible_loads[0] == il
    assert RZ.interruptible_loads[0] == il
    assert node.interruptible_loads[0] == il
    assert company.interruptible_loads[0] == il


def test_branch_creation():

    operator = SystemOperator()
    company = Company("company")
    RZ = ReserveZone("RZ", operator)
    node1 = Node("node1", operator, RZ, demand=154)
    node2 = Node("node2", operator, RZ, demand=154)

    branch = Branch(operator, node1, node2, risk=True, capacity=500)

    assert branch.risk == True
    assert branch.capacity == 500

    assert branch.name == 'node1_node2'

    assert branch.sending_node == node1
    assert branch.receiving_node == node2

    assert operator.branches[0] == branch


def test_station_offer():

    operator = SystemOperator()
    company = Company("company")
    RZ = ReserveZone("RZ", operator)
    node = Node("node", operator, RZ, demand=154)

    station = Station('station', operator, node, company, capacity=300)

    station.add_energy_offer(50, 100)

    station.add_reserve_offer(25, 300, 0.3)

    assert station.energy_price == 50
    assert station.energy_offer == 100
    assert station.reserve_price == 25
    assert station.reserve_offer == 300
    assert station.reserve_proportion == 0.3

def test_il_offer():

    operator = SystemOperator()
    company = Company("company")
    RZ = ReserveZone("RZ", operator)
    node = Node("node", operator, RZ, demand=154)
    il = InterruptibleLoad('il', operator, node, company)

    il.add_reserve_offer(100, 200)

    assert il.reserve_price == 100
    assert il.reserve_offer == 200
