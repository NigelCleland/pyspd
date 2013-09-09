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
