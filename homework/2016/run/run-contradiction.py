#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../contradiction')
import SAT
pfile = sys.argv[1]
SAT.solve(pfile)
os.rename(pfile[:-4]+'_solution.txt', sys.argv[2])
