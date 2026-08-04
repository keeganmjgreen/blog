from math import pi

import pyomo.environ as pyo

model = pyo.AbstractModel()


# Sets


model.load_bus_index = pyo.Set()
model.generator_bus_index = pyo.Set()
model.slack_bus_index = pyo.Set()
model.bus_index = (
    model.load_bus_index | model.generator_bus_index | model.slack_bus_index
)
model.nonzero_pq_pair_index = pyo.Set(
    doc="Index of all nonzero (price, quantity) pairs, concatenated from all generator offers"
)


# Parameters


model.pq_pair_to_bus = pyo.Param(
    model.nonzero_pq_pair_index,
    within=(model.generator_bus_index | model.slack_bus_index),
    doc="Map from a (price, quantity) pair to a generator or slack bus",
)
model.prices = pyo.Param(
    model.nonzero_pq_pair_index,
    doc="Flat list of nonzero prices per MWh concatenated from all generators' (price, quantity) pairs",
)
model.quantity_steps = pyo.Param(
    model.nonzero_pq_pair_index,
    within=pyo.PositiveReals,
    doc="Flat list of quantity steps concatenated from all generators' (price, quantity pairs)",
)

model.conductances = pyo.Param(
    model.bus_index,
    model.bus_index,
    within=pyo.Reals,
    doc="Real component of the admittance matrix",
)
model.susceptances = pyo.Param(
    model.bus_index,
    model.bus_index,
    within=pyo.Reals,
    doc="Imaginary component of the admittance matrix",
)

model.load_real_powers = pyo.Param(model.load_bus_index, within=pyo.Reals)
model.load_reactive_powers = pyo.Param(model.load_bus_index, within=pyo.Reals)

model.fixed_voltage_magnitudes = pyo.Param(
    model.generator_bus_index | model.slack_bus_index
)

model.min_voltage_magnitudes = pyo.Param(model.bus_index)
model.max_voltage_magnitudes = pyo.Param(model.bus_index)

model.max_current_magnitudes = pyo.Param(
    model.bus_index, model.bus_index, within=pyo.NonNegativeReals
)

# Variables


def real_power_bounds(m: pyo.Model, pq_pair_i: int):
    return (0, m.quantity_steps[pq_pair_i])


model.generator_real_powers = pyo.Var(
    model.nonzero_pq_pair_index,
    within=pyo.NonNegativeReals,
    bounds=real_power_bounds,
    doc="Real power dispatch for each generator (price, quantity) pair",
)

model.reactive_powers = pyo.Var(model.bus_index, within=pyo.Reals)


def voltage_magnitude_bounds(m: pyo.Model, bus_i: int):
    return (m.min_voltage_magnitudes[bus_i], m.max_voltage_magnitudes[bus_i])


model.voltage_magnitudes = pyo.Var(model.bus_index, bounds=voltage_magnitude_bounds)
model.voltage_angles = pyo.Var(model.bus_index, within=pyo.Reals, bounds=(-pi, pi))


# Objective: Minimize system cost


model.cost = pyo.Objective(
    expr=pyo.sum_product(model.prices, model.generator_real_powers)
)


# Constraints

## Power Flow Equations (Bus Injection Model)


def real_power_flow_rule(m: pyo.Model, bus_i: int):
    injections = [
        m.generator_real_powers[pq_pair_i]
        for pq_pair_i in m.nonzero_pq_pair_index
        if m.pq_pair_to_bus[pq_pair_i] == bus_i
    ]
    if bus_i in m.load_bus_index:
        injections.append(m.load_real_powers[bus_i])
    withdrawals = [
        m.voltage_magnitudes[bus_i]
        * m.voltage_magnitudes[bus_k]
        * (
            m.conductances[bus_i, bus_k]
            * pyo.cos(m.voltage_angles[bus_i] - m.voltage_angles[bus_k])
            + m.susceptances[bus_i, bus_k]
            * pyo.sin(m.voltage_angles[bus_i] - m.voltage_angles[bus_k])
        )
        for bus_k in m.bus_index
    ]
    return sum(injections) == sum(withdrawals)


def reactive_power_flow_rule(m: pyo.Model, bus_i: int):
    injection = m.reactive_powers[bus_i]
    withdrawals = [
        m.voltage_magnitudes[bus_i]
        * m.voltage_magnitudes[bus_k]
        * (
            m.conductances[bus_i, bus_k]
            * pyo.sin(m.voltage_angles[bus_i] - m.voltage_angles[bus_k])
            - m.susceptances[bus_i, bus_k]
            * pyo.cos(m.voltage_angles[bus_i] - m.voltage_angles[bus_k])
        )
        for bus_k in m.bus_index
    ]
    return injection == sum(withdrawals)


model.real_power_flow_constraint = pyo.Constraint(
    model.bus_index, rule=real_power_flow_rule
)
model.reactive_power_flow_constraint = pyo.Constraint(
    model.bus_index, rule=reactive_power_flow_rule
)


## Branch Loading Constraint


def branch_loading_rule(m: pyo.Model, bus_i: int, bus_k: int):
    current_magnitude = pyo.sqrt(
        (
            m.voltage_magnitudes[bus_i] * pyo.cos(m.voltage_angles[bus_i])
            - m.voltage_magnitudes[bus_k] * pyo.cos(m.voltage_angles[bus_k])
        )
        ** 2
        + (
            m.voltage_magnitudes[bus_i] * pyo.sin(m.voltage_angles[bus_i])
            - m.voltage_magnitudes[bus_k] * pyo.sin(m.voltage_angles[bus_k])
        )
        ** 2
    ) * pyo.sqrt(m.conductances[bus_i, bus_k] ** 2 + m.susceptances[bus_i, bus_k] ** 2)
    return current_magnitude <= m.max_current_magnitudes[bus_i, bus_k]


model.branch_loading_constraint = pyo.Constraint(
    model.bus_index, model.bus_index, rule=branch_loading_rule
)


## Bus Type Constraints


def load_bus_reactive_power_rule(m: pyo.Model, bus_i: int):
    return m.reactive_powers[bus_i] == m.load_reactive_powers[bus_i]


def fixed_voltage_magnitude_rule(m: pyo.Model, bus_i: int):
    return m.voltage_magnitudes[bus_i] == m.fixed_voltage_magnitudes[bus_i]


def slack_bus_voltage_angle_rule(m: pyo.Model, bus_i: int):
    return m.voltage_angles[bus_i] == 0


model.load_bus_reactive_power_constraint = pyo.Constraint(
    model.load_bus_index, rule=load_bus_reactive_power_rule
)
model.fixed_voltage_magnitude_constraint = pyo.Constraint(
    model.generator_bus_index | model.slack_bus_index, rule=fixed_voltage_magnitude_rule
)
model.slack_bus_voltage_angle_constraint = pyo.Constraint(
    model.slack_bus_index, rule=slack_bus_voltage_angle_rule
)
