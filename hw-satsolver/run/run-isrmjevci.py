#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../isrmjevci')
import functions
fileInput = sys.argv[1]
functions.satSolver(fileInput)
os.rename(fileInput.replace(".txt", "_solution.txt"), sys.argv[2])
