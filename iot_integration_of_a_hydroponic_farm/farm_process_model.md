# Farm Process Model

A farm process model was developed to simulate growth day-by-day for the life cycle of the crop. It models the consumption of energy and resources and is designed for minimizing the operating cost of a full-size hydroponic farm; an optimization problem is formulated.

The following graph depicts the dependencies between parameters and variables for each iteration of the plant growth model, whose state is updated for each day. The diagram was generated programmatically.

```{figure} img/EPIC.mermaid.png
:width: 100%

Plant growth model.
```

The design variables are (1) the growing time in days $n$, (2) the temperature $T$ maintained ideally of both the air and growth medium, (3) the water content $\mathit{SW}$ of the growth medium, (4) the given plant uptake rate $\mathit{UN}$ of nitrogen, (5) the given plant uptake rate $\mathit{UP}$ of phosphorus, (6) the solar radiation $\mathit{RA}$, and (7) the simulated daylength $\mathit{HRLT}$:

$$
\mathbf{x} = [n, T, \mathit{SW}, \mathit{UN}, \mathit{UP}, \mathit{RA}, \mathit{HRLT}\,]
$$

All but the first design variable are repeated for each of the $n$ days upon entry to the E.P.I.C. plant growth model. Together with a number of crop parameters, this grants us access to (1) the plant water usage $u$, (2) the daily-accumulated biomass $B$, (3) the crop height $\mathit{CHT}$ if desired as a metric for plant growth, and (4) the amount of economic crop yield $\mathit{YLD}$ that can be removed from the hydroponic farm:

$$
(u, B, \mathit{CHT}, \mathit{YLD}) = \mathit{EPIC}\,(n, T, \mathit{SW}, \mathit{UN}, \mathit{UP}, \mathit{RA}, \mathit{HRLT}\,)
$$

See [The EPIC Crop Growth Model](https://www.ars.usda.gov/ARSUserFiles/30980500/The%20EPIC%20Crop%20Growth%20Model.pdf) by Williams et al. for more information

Now, the energy for pumping water, heating the water/biomass, and running the lighting are prescribed functions of intermediate or design variables:

$$
\begin{aligned}
& \text{pumping energy} = f_1(\mathit{SW}) \\
& \text{heating energy} = f_2(n, T, B, \text{pumping energy}) \\
& \text{lighting energy} = f_3(n, \mathit{RA})
\end{aligned}
$$

With the energy use of the water aerator assumed to be fixed, the remaining variable energy cost is:

$$
\begin{aligned}
& \text{variable energy use} = \text{lighting energy} + \text{heating energy} + \text{pumping energy} \\
& \text{variable energy cost} = \text{variable energy use} \cdot \text{price per kWh}
\end{aligned}
$$

The cost of water is a function of the water usage $u$:

$$
\begin{aligned}
& \text{water volume} = f_4(u) \\
& \text{water cost} = \text{water volume} \cdot \text{price per L water}
\end{aligned}
$$

The mass of nitrogen and phosphorus nutrients consumed are functions of their plant uptake rates:

$$
\begin{aligned}
& m_\mathrm{N} = f_5(\mathit{UN}) \\
& m_\mathrm{P} = f_6(\mathit{UP})
\end{aligned}
$$

The cost of nutrients is minimally:

$$
\begin{aligned}
\text{N cost} = m_\mathrm{N} \cdot \text{price per kg N} \\
\text{P cost} = m_\mathrm{P} \cdot \text{price per kg P} \\
\text{nutrient cost} = \text{N cost} + \text{P cost}
\end{aligned}
$$

The value of the objective function is then computed by:

$$
\begin{aligned}
& \text{variable cost} = \text{variable energy cost} + \text{water cost} + \text{nutrient cost} \\
& \text{revenue} = (\mathit{YLD} \cdot \text{effective farm area}) \cdot \text{crop unit price} \\
& y = \text{variable cost} - \text{revenue}
\end{aligned}
$$
