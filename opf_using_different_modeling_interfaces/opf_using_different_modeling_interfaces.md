# Formulating the Optimal Power Flow Problem Using Pyomo, Gurobipy, and AMPL

The optimal power flow (OPF) problem is vital to the stable and cost-effective operation of the electrical grid. See [here](#the-optimal-power-flow-opf-problem) for a full derivation and formulation using the bus injection model, and [here](#supply_and_demand_of_electricity_higher_dimensional_optimization_problems) for the approach we'll be taking to incorporate generator offers in the electricity market.

Like any other optimization problem, OPF must be formulated in a standard format in order to interface with an optimization algorithm (a solver). This allows the decision variables, the constraints, the objective, etc. to be supplied to the solver, and the final solution to be extracted. Optimization modeling interfaces like [Pyomo](https://www.pyomo.org/), [Gurobipy](https://www.gurobi.com/resources/faq/gurobipy), and [AMPL](https://ampl.com/) are designed to make this easy, speaking the same language&mdash;sets, parameters, variables, and so on&mdash;that's common when formulating optimization problems.

Pyomo and Gurobipy are implemented as Python libraries&mdash;meaning that, although they have some overhead, the formulation and solving of optimization problems can easily be integrated into larger programs. AMPL is a leaner language with more convenient syntax tailor-made for formulating optimization problems, but is more cumbersome to use with programming languages like Python. Gurobi, the developer of Gurobipy, provides similar libraries for other programming languages.

Pyomo and AMPL are solver-agnostic; they can be used with a variety of free and commercial solvers. Gurobipy, on the other hand, is exclusively for use with Gurobi's proprietary solver.

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

## Appendix: Deriving the branch loading constraint

The branch loading constraint specifies that the apparent power flowing into any branch (denoted $ik$) from either attached bus (denoted $i$) cannot exceed the branch's rated maximum:

$$
|S_{ik}| \leq S_{ik}^{\:\! \text{max}}
$$

This needs to be expressed in terms of the decision variables for the voltage magnitudes ($|V_i|$, $|V_k|$) and voltage angles ($\delta_i$, $\delta_k$). The complex power $S_{ik}$ is given by:

$$
S_{ik} = V_{\! i} \left( V_{\! i} \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) - V_k \frac{1}{a_{ik}^*} y_{ik} \right)
$$

For simplicity at the expense of accuracy, we assume $a_{ik} = 1$ (no off-nominal turns ratios) and $y_{ik}^\text{Sh} = 0$ (no shunt admittances):

$$
S_{ik} = V_{\! i} \, (V_{\! i} - V_k)^* \, y_{ik}^*
$$

Furthermore, because $Y_{\! ik} = - y_{ik}$ when $a_{ik} = 1$, where $Y$ is the bus admittance matrix, we can rewrite $S_{ik}$ as:

$$
S_{ik} = - V_{\! i} \, (V_{\! i} - V_k)^* \, Y_{\! ik}^*
$$

This allows us to use only the bus admittance matrix, not the separate branch-from-bus and branch-to-bus admittance matrices. Finally, the apparent power is as follows, where $G$ and $B$ are the real and imaginary parts of the bus admittance matrix.

$$
\begin{aligned}
|S_{ik}|
& = |V_{\! i}| \, |V_{\! i} - V_k| \, |Y_{\! ik}| \\
& = |V_{\! i}| \sqrt{(|V_{\! i}| \cos \delta_i - |V_k| \cos \delta_k)^2 + (|V_{\! i}| \sin \delta_i - |V_k| \sin \delta_k)^2} \sqrt{G_{ik}^2 + B_{ik}^2}
\end{aligned}
$$
