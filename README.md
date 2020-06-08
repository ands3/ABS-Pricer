# ABS-Pricer

This program takes a csv file of thousands of fixed rate loans. It then uses them to build a loan pool via inheritance, mixin, and composition. It similarly builds up the structured security (the combination of the tranches) via inheritance and composition. After the loan pool and structured security are constructed, nested Monte Carlo simulations occur. In the inner layer, the program iterates over periods, simulating potential loan defaults, paying the tranches by seniority, and outputting the resulting cash flows and risk metrics. In the outer layer, the outputted risk metrics are used to determine the implied tranche rates. Additionally, multiprocessing is incorporated to speed up the nested simulations.

In summary, this program does the following:
1) Price an asset-backed security, with potential loan defaults, determine risk metrics (IRR, DIRR, letter rating, and WAL), and output the cash flows that occurred each period for both the loan pool and the tranches.
2) Determine the fair tranche rates.

UPDATES
=======

6/7/2020: migrated everything from Python 2 to Python 3
