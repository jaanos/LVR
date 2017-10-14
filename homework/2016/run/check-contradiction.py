#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../contradiction')
import SAT
with open(sys.argv[2]) as f:
    print(SAT.checker(sys.argv[1], f.readline()))
