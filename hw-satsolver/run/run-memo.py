#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../memo')
import SAT_Solver
input = sys.argv[1]
SAT_Solver.solve(input, pure = True, guess_key = "frequent")
os.rename(input.split(".")[0] + "_solution.txt", sys.argv[2])
