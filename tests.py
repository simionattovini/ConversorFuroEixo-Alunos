import pandas as pd
import backend_tools as bt
import tables as tb

instr = '40H7/g6'
indata = bt.input_parser(instr)
bt.input_validator(indata)
axledata = bt.calculate_asymmetric_tol_dimension_axle(indata)
print(axledata)
holedata = bt.calculate_asymmetric_tol_dimension_hole(indata)
print(holedata)
