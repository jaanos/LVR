#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../memo')
import SAT_Solver
SAT_Solver.solve(sys.argv[1], sys.argv[2], pure = True, guess_key = "frequent")
