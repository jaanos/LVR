#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '../goodboy')
import SAT_Solver
nrOfVars, exp = SAT_Solver.dataInput(sys.argv[1])
satisfiable, solution = SAT_Solver.solveSAT(exp)
with open(sys.argv[2], 'w') as out:
    if satisfiable:
        out.write(' '.join([int(x) for x in solution]))
    else:
        out.write('Not satisfiable')
