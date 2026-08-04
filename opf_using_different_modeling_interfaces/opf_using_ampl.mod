# Sets

set LOAD_BUS_INDEX;
set GENERATOR_BUS_INDEX;
set SLACK_BUS_INDEX;
set BUS_INDEX = LOAD_BUS_INDEX union GENERATOR_BUS_INDEX union SLACK_BUS_INDEX;
# Index of all nonzero (price, quantity) pairs, concatenated from all generator offers:
set NONZERO_PQ_PAIR_INDEX;

# Parameters

param pi := acos(-1);

# Map from a (price, quantity) pair to a generator or slack bus:
param pq_pair_to_bus {pq_pair_i in NONZERO_PQ_PAIR_INDEX}
    in (GENERATOR_BUS_INDEX union SLACK_BUS_INDEX);
# Flat list of nonzero prices per MWh concatenated from all generators'
# (price, quantity) pairs:
param prices {NONZERO_PQ_PAIR_INDEX};
# Flat list of quantity steps concatenated from all generators' (price, quantity pairs):
param quantity_steps {NONZERO_PQ_PAIR_INDEX} > 0;

# Real component of the admittance matrix:
param conductances {BUS_INDEX, BUS_INDEX};
# Imaginary component of the admittance matrix:
param susceptances {BUS_INDEX, BUS_INDEX};

param load_real_powers {LOAD_BUS_INDEX};
param load_reactive_powers {LOAD_BUS_INDEX};

param fixed_voltage_magnitudes {GENERATOR_BUS_INDEX union SLACK_BUS_INDEX};

param min_voltage_magnitudes {BUS_INDEX};
param max_voltage_magnitudes {BUS_INDEX};

param max_current_magnitudes {BUS_INDEX, BUS_INDEX} >= 0;

# Variables

# Real power dispatch for each generator (price, quantity) pair:
var GeneratorRealPowers {pq_pair_i in NONZERO_PQ_PAIR_INDEX}
    >= 0, <= quantity_steps[pq_pair_i];

var ReactivePowers {BUS_INDEX};

var VoltageMagnitudes {bus_i in BUS_INDEX}
    >= min_voltage_magnitudes[bus_i], <= max_voltage_magnitudes[bus_i];

var VoltageAngles {BUS_INDEX} >= -pi, <= pi;

# Objective: Minimize system cost

minimize Cost:
    sum {pq_pair_i in NONZERO_PQ_PAIR_INDEX} prices[pq_pair_i] * GeneratorRealPowers[pq_pair_i];

# Constraints

## Power Flow Equations (Bus Injection Model)

subject to RealPowerFlowConstraint {bus_i in BUS_INDEX}:
    sum {pq_pair_i in NONZERO_PQ_PAIR_INDEX: pq_pair_to_bus[pq_pair_i] == bus_i}
        GeneratorRealPowers[pq_pair_i]
    + (if bus_i in LOAD_BUS_INDEX then load_real_powers[bus_i] else 0)
    == sum {bus_k in BUS_INDEX} (
        VoltageMagnitudes[bus_i]
        * VoltageMagnitudes[bus_k]
        * (
            conductances[bus_i, bus_k]
            * cos(VoltageAngles[bus_i] - VoltageAngles[bus_k])
            + susceptances[bus_i, bus_k]
            * sin(VoltageAngles[bus_i] - VoltageAngles[bus_k])
        )
    );

subject to ReactivePowerFlowConstraint {bus_i in BUS_INDEX}:
    ReactivePowers[bus_i] == sum {bus_k in BUS_INDEX} (
        VoltageMagnitudes[bus_i]
        * VoltageMagnitudes[bus_k]
        * (
            conductances[bus_i, bus_k]
            * sin(VoltageAngles[bus_i] - VoltageAngles[bus_k])
            - susceptances[bus_i, bus_k]
            * cos(VoltageAngles[bus_i] - VoltageAngles[bus_k])
        )
    );

## Branch Loading Constraint

subject to BranchLoadingConstraint {bus_i in BUS_INDEX, bus_k in BUS_INDEX}:
    sqrt(
        (
            VoltageMagnitudes[bus_i] * cos(VoltageAngles[bus_i])
            - VoltageMagnitudes[bus_k] * cos(VoltageAngles[bus_k])
        )^2
        + (
            VoltageMagnitudes[bus_i] * sin(VoltageAngles[bus_i])
            - VoltageMagnitudes[bus_k] * sin(VoltageAngles[bus_k])
        )^2
    ) * sqrt(
        conductances[bus_i, bus_k]^2 + susceptances[bus_i, bus_k]^2
    ) <= max_current_magnitudes[bus_i, bus_k];

# Bus Type Constraints

subject to LoadBusReactivePowerConstraint {bus_i in LOAD_BUS_INDEX}:
    ReactivePowers[bus_i] == load_reactive_powers[bus_i];

subject to FixedVoltageMagnitudeConstraint {bus_i in GENERATOR_BUS_INDEX union SLACK_BUS_INDEX}:
    VoltageMagnitudes[bus_i] == fixed_voltage_magnitudes[bus_i];

subject to SlackBusVoltageAngleConstraint {bus_i in SLACK_BUS_INDEX}:
    VoltageAngles[bus_i] == 0;
