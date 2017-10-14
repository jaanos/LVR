#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../salt-n-pepa/satsolver')
import satSolverOpt
inputFile = sys.argv[1]
satSolverOpt.solve(inputFile)
split = inputFile.split('.')
extension = split[len(split)-1]
file = '.'.join(split[:-1])
os.rename(file + '_sol.' + extension, sys.argv[2])
