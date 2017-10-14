#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../pythonsolver/popravljenSAT')
import SATsolvePopravljen
SATsolvePopravljen.SATsolverDimacs(sys.argv[1], sys.argv[2])
