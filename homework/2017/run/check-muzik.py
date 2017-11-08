#!/usr/bin/env python3.6
import sys
sys.path.insert(0, '../muzik')
from Solution_Checker import check_solution
try:
    if check_solution(sys.argv[2], sys.argv[1]):
        print("Rešitev je pravilna")
    else:
        sys.exit(1)
except Exception as ex:
    print("Napaka: %s" % ex)
    sys.exit(2)
