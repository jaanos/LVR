#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../biblethump')
import SAT_solver
SAT_solver.sat(sys.argv[1], sys.argv[2])
