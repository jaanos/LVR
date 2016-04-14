#!/usr/bin/env python

import os
import sys
import subprocess

from data import progs, checks, tests

if len(sys.argv) > 1:
    teams = sys.argv[1:]
else:
    teams = sorted(progs.keys())

def checkSolution(testfile, resfile, checker):
    print('\nRunning %s ...' % checker)
    sys.stdout.flush()
    p = subprocess.Popen(['./%s' % checker, testfile, resfile])
    ret = p.wait()
    print('Exited with code %d' % ret)
    sys.stdout.flush()

if __name__ == '__main__':
    for test in tests:
        testfile = '../dimacs/%s' % test
        for team in teams:
            resfile = 'results/%s_%s' % (team, test)
            try:
                if os.stat(resfile).st_size <= 32:
                    continue
            except OSError:
                continue
            print('\n=====================================')
            print('\nChecking the solution to %s by %s ...' % (test, team))
            sys.stdout.flush()
            for checker in checks:
                checkSolution(testfile, resfile, checker)
