# Formulating the Optimal Power Flow Problem Using Pyomo, Gurobipy, and AMPL

The optimal power flow (OPF) problem is vital to the stable and cost-effective operation of the electrical grid. See [here](#the-optimal-power-flow-opf-problem) for a full derivation and formulation using the bus injection model, and [here](#supply_and_demand_of_electricity_higher_dimensional_optimization_problems) for the approach we'll be taking to incorporate generator offers in the electricity market.

Like any other optimization problem, OPF must be formulated in a standard format in order to interface with an optimization algorithm (a solver). This allows the decision variables, the constraints, the objective, etc. to be supplied to the solver, and the final solution to be extracted. Optimization modeling interfaces like [Pyomo](https://www.pyomo.org/), [Gurobipy](https://www.gurobi.com/resources/faq/gurobipy), and [AMPL](https://ampl.com/) are designed to make this easy, speaking the same language&mdash;sets, parameters, variables, and so on&mdash;that's common when formulating optimization problems.

Pyomo and Gurobipy are implemented as Python libraries&mdash;meaning that, although they have some overhead, the formulation and solving of optimization problems can easily be integrated into larger programs. AMPL is a leaner language with more convenient syntax tailor-made for formulating optimization problems, but is more cumbersome to use with programming languages like Python. Gurobi, the developer of Gurobipy, provides similar libraries for other programming languages.

Pyomo and AMPL are solver-agnostic; they can be used with a variety of free and commercial solvers. Gurobipy, on the other hand, is exclusively for use with Gurobi's proprietary solver.

<!-- Deriving branch loading constraint:
|I_ik|
= |(V_i - V_k) * Y_ik|
= |(|V_i| cos(delta_i) + j |V_i| sin(delta_i) - |V_k| cos(delta_k) - j |V_k| sin(delta_k)) * (G_ik + j B_ik)|
= sqrt((|V_i| cos(delta_i) - |V_k| cos(delta_k))^2 + (|V_i| sin(delta_i) - j |V_k| sin(delta_k))^2) * sqrt(G_ik^2 + B_ik^2) -->

## Pyomo

```{literalinclude} opf_using_pyomo.py
:filename: false
:language: python
```

Resources: [Mathematical Modeling · Pyomo](https://pyomo.readthedocs.io/en/stable/getting_started/pyomo_overview/math_modeling.html) | See also: [Pyomo Network](https://pyomo.readthedocs.io/en/stable/explanation/modeling/network.html)

## Gurobipy

```{literalinclude} opf_using_gurobi.py
:filename: false
```

Resources: [Gurobi's example of unit commitment](https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/power_generation/optimize_power_schedule.ipynb)

## AMPL

```{literalinclude} opf_using_ampl.mod
:filename: false
```

Resources: [AMPL introduction](https://dev.ampl.com/ampl/introduction.html) | [AMPL expressions](https://mp.ampl.com/modeling-expressions.html) | [AMPL's example of unit commitment](https://colab.ampl.com/notebooks/unit-commitment-minlp-with-knitro.html) | [AMPL's example of stochastic optimization for economic dispatch](https://ampl.com/mo-book/notebooks/09/economicdispatch.html)
