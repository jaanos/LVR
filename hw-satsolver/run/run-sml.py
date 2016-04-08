#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '../sml/Solver')
import read_file
import sat
input_file = read_file.readDimacs(sys.argv[1])
sol = sat.solve(input_file,[])
with open(sys.argv[2], 'w') as out:
    if sol == False:
        out.write("No solution found")
    else:
        out.write(' '.join([str(k if v else -k) for k, v in sat.buildSoultion(sol).items()]))
