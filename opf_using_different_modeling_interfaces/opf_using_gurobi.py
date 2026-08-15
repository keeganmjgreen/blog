from math import inf, pi

import gurobipy as gp
from gurobipy import nlfunc

model = gp.Model("opf")

# Sets

type LoadBusIdx = int
type GeneratorBusIdx = int
type SlackBusIdx = int
type BusIdx = LoadBusIdx | GeneratorBusIdx | SlackBusIdx

load_bus_index: set[LoadBusIdx] = set()
generator_bus_index: set[GeneratorBusIdx] = set()
slack_bus_index: set[SlackBusIdx] = set()
bus_index: set[BusIdx] = load_bus_index | generator_bus_index | slack_bus_index

type PqPairIdx = int

nonzero_pq_pair_index = set[PqPairIdx]()

# Parameters

# Map from a (price, quantity) pair to a generator or slack bus:
pq_pair_to_bus: dict[PqPairIdx, BusIdx] = {}
# Flat list of nonzero prices per MWh concatenated from all generators'
# (price, quantity) pairs:
prices: dict[PqPairIdx, float] = {}
# Flat list of quantity steps concatenated from all generators' (price, quantity pairs):
quantity_steps: dict[PqPairIdx, float] = {}

# Real component of the admittance matrix:
conductances: dict[BusIdx, dict[BusIdx, float]] = {}
# Imaginary component of the admittance matrix:
susceptances: dict[BusIdx, dict[BusIdx, float]] = {}

load_real_powers: dict[LoadBusIdx, float] = {}
load_reactive_powers: dict[LoadBusIdx, float] = {}

fixed_voltage_magnitudes: dict[GeneratorBusIdx | SlackBusIdx, float] = {}

min_voltage_magnitudes: dict[BusIdx, float] = {}
max_voltage_magnitudes: dict[BusIdx, float] = {}

max_apparent_powers: dict[BusIdx, dict[BusIdx, float]] = {}

# Variables

generator_real_powers = model.addVars(nonzero_pq_pair_index, lb=0, ub=quantity_steps)
reactive_powers = model.addVars(bus_index, lb=-inf, ub=inf)
voltage_magnitudes = model.addVars(
    bus_index, lb=min_voltage_magnitudes, ub=max_voltage_magnitudes
)
voltage_angles = model.addVars(bus_index, lb=-pi, ub=pi)

# Objective: Minimize system cost

model.setObjective(
    gp.quicksum(
        prices[pq_pair_i] * generator_real_powers[pq_pair_i]
        for pq_pair_i in nonzero_pq_pair_index
    )
)

# Constraints

## Power Flow Equations (Bus Injection Model)

real_power_withdrawals = model.addVars(bus_index, lb=-inf, ub=inf)
model.addConstrs(
    gp.quicksum(
        generator_real_powers[pq_pair_i]
        for pq_pair_i in nonzero_pq_pair_index
        if pq_pair_to_bus[pq_pair_i] == bus_i
    )
    + (load_real_powers[bus_i])
    == real_power_withdrawals[bus_i]
    for bus_i in bus_index
)
model.addConstrs(
    real_power_withdrawals[bus_i]
    == gp.quicksum(
        voltage_magnitudes[bus_i]
        * voltage_magnitudes[bus_k]
        * (
            conductances[bus_i][bus_k]
            * nlfunc.cos(voltage_angles[bus_i] - voltage_angles[bus_k])
            + susceptances[bus_i][bus_k]
            * nlfunc.sin(voltage_angles[bus_i] - voltage_angles[bus_k])
        )
        for bus_k in bus_index
    )
    for bus_i in bus_index
)

model.addConstrs(
    reactive_powers[bus_i]
    == gp.quicksum(
        voltage_magnitudes[bus_i]
        * voltage_magnitudes[bus_k]
        * (
            conductances[bus_i][bus_k]
            * nlfunc.sin(voltage_angles[bus_i] - voltage_angles[bus_k])
            - susceptances[bus_i][bus_k]
            * nlfunc.cos(voltage_angles[bus_i] - voltage_angles[bus_k])
        )
        for bus_k in bus_index
    )
    for bus_i in bus_index
)

## Branch Loading Constraint

model.addConstrs(
    voltage_magnitudes[bus_i]
    * nlfunc.sqrt(
        nlfunc.square(
            voltage_magnitudes[bus_i] * nlfunc.cos(voltage_angles[bus_i])
            - voltage_magnitudes[bus_k] * nlfunc.cos(voltage_angles[bus_k])
        )
        + nlfunc.square(
            voltage_magnitudes[bus_i] * nlfunc.sin(voltage_angles[bus_i])
            - voltage_magnitudes[bus_k] * nlfunc.sin(voltage_angles[bus_k])
        )
    )
    * nlfunc.sqrt(
        nlfunc.square(conductances[bus_i][bus_k])
        + nlfunc.square(susceptances[bus_i][bus_k])
    )
    <= max_apparent_powers[bus_i, bus_k]
    for bus_k in bus_index
    for bus_i in bus_index
)

## Bus Type Constraints

model.addConstrs(
    reactive_powers[bus_i] == load_reactive_powers[bus_i] for bus_i in load_bus_index
)
model.addConstrs(
    voltage_magnitudes[bus_i] == fixed_voltage_magnitudes[bus_i]
    for bus_i in generator_bus_index | slack_bus_index
)
model.addConstrs(voltage_angles[bus_i] == 0 for bus_i in slack_bus_index)
