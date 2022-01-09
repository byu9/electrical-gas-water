# RISF Sharing Page

Online backup of source code for RISF Fall 2021 (Water-Energy Nexus).


## Compiling the Contract

Run `pdflatex` twice to fully compile the glossary.

```
cd ./doc
pdflatex \\nonstopmode\\input contract.tex
makeglossaries contract
pdflatex \\nonstopmode\\input contract.tex
```


## Units of Measure

Note during discussion with Xiaochu, some constraints involving integrals with
time (such as that of electrical/gas state of charge) implicitly multiplies by
one unit timestep in the equation. As a result:

1. Time points in the scheduling horizon must be spaced equally (uniform sample
   rate)

1. Units of measure of the time step will affect the unit of measure of
   integrals involving time. For example, if the time points in the scheduling
   horizon is one hour apart, the unit of measure for the battery state of
   charge will also involve hours, for example, in watt-hours.

See (Contract)[contract.tex] for units of measure
