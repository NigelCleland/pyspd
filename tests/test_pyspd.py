#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyspd
----------------------------------

Tests for `pyspd` module.
"""

import pytest
from pyspd import *

def setup_function(function):
    operator = SystemOperator()
    company = Company("company")
    RZ = ReserveZone("RZ", operator)
    node = Node("node", operator, RZ, demand=154)


@setup_function
def test_operator_creation():
    assert isinstance(operator, SystemOperator)

@setup_function
def test_rz_creation():

    assert RZ.name  == "RZ"
    assert RZ.nodes == []
    assert RZ.stations == []
    assert RZ.interruptible_loads == []

    assert operator.reserve_zones[0] == RZ

@setup_function
def test_node_creation():
    assert node.name == 'node'
    assert operator.nodes[0] == node
    assert node.RZ == RZ
    assert RZ.nodes[0] == node
    assert node.demand == 154

@setup_function
def test_company_creation():
    assert company.name == 'company'
    assert company.stations == []
    assert company.interruptible_loads == []

@setup_function
def test_station_creation():
    station = Station("station", operator, node, company, capacity=500)

    assert station.name == "station"
    assert station.capacity == 500

    assert operator.stations[0] == station
    assert company.stations[0] == station
    assert node.stations[0] == station
    assert RZ.stations[0] == station

@setup_function
def test_il_creation():
    il = InterruptibleLoad('IL', operator, node, company)

    assert il.name == "IL"
    assert operator.interruptible_loads[0] == il
    assert RZ.interruptible_loads[0] == il
    assert node.interruptible_loads[0] == il
    assert company.interruptible_loads[0] == il

@setup_function
def test_branch_creation():

    node2 = Node("node2", operator, RZ, demand=154)

    branch = Branch(operator, node1, node2, risk=True, capacity=500)

    assert branch.risk == True
    assert branch.capacity == 500

    assert branch.name == 'node1_node2'

    assert branch.sending_node == node1
    assert branch.receiving_node == node2

    assert operator.branches[0] == branch

@setup_function
def test_station_offer():
    station = Station('station', operator, node, company, capacity=300)
    station.add_energy_offer(50, 100)
    station.add_reserve_offer(25, 300, 0.3)

    assert station.energy_price == 50
    assert station.energy_offer == 100
    assert station.reserve_price == 25
    assert station.reserve_offer == 300
    assert station.reserve_proportion == 0.3

@setup_function
def test_il_offer():
    il = InterruptibleLoad('il', operator, node, company)

    il.add_reserve_offer(100, 200)

    assert il.reserve_price == 100
    assert il.reserve_offer == 200

@setup_function
def test_operator_station_parameters():
    station = Station('station', operator, node, company, capacity=300)

    station.add_energy_offer(50, 100)

    station.add_reserve_offer(25, 300, 0.3)

    operator._station_parameters('P55')

    assert operator.energy_station_names[0] == 'P55_station'
    assert operator.energy_station_capacity['P55_station'] == 100
    assert operator.energy_station_price['P55_station'] == 50

    assert operator.reserve_station_names[0] == 'P55_station'
    assert operator.reserve_station_capacity['P55_station'] == 300
    assert operator.reserve_station_price['P55_station'] == 25
    assert operator.reserve_station_proportion['P55_station'] == 0.3

@setup_function
def test_operator_il_parameters():

    il = InterruptibleLoad('il', operator, node, company)
    il.add_reserve_offer(100, 200)

    operator._interruptible_load_parameters('P55')

    assert operator.reserve_IL_names[0] == 'P55_il'
    assert operator.reserve_IL_price['P55_il'] == 100
    assert operator.reserve_IL_capacity['P55_il'] == 200

@setup_function
def test_operator_node_parameters():

    station = Station('station', operator, node, company, capacity=300)

    operator._node_parameters()
    assert operator.node_names[0] == 'P55_node'
    assert operator.nodal_demand['P55_node'] == 154

    assert operator.nodal_stations['P55_node'][0] == 'P55_station'

@setup_function
def test_operator_branch_parameters():

    node2 = Node('node2', operator, RZ, demand=200)

    branch = Branch(operator, node, node2, capacity=150, risk=True)

    operator._transmission_parameters('P55')

    assert operator.branch_names[0] == 'P55_node_node2'
    assert operator.node_flow_map['P55_node'][0] == 'P55_node_node2'
    assert operator.node_flow_map['P55_node2'][0] == 'P55_node_node2'
    assert operator.node_flow_direction['P55_node']['P55_node_node2'] == 1
    assert operator.node_flow_direction['P55_node2']['P55_node_node2'] == -1

    assert operator.reserve_zone_flow_map['P55_RZ'] == []
    assert operator.reserve_zone_flow_direction['P55_RZ']['P55_node_node2'] == None
