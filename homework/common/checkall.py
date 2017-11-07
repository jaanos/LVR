#!/usr/bin/env python

import os
import sys
import subprocess

from .args import parseArgs

def checkSolution(testfile, resfile, checker):
    print('\nRunning %s ...' % checker)
    sys.stdout.flush()
    p = subprocess.Popen(['./%s' % checker, testfile, resfile])
    ret = p.wait()
    print('Exited with code %d' % ret)
    sys.stdout.flush()

def run(data):
    teams, tests = parseArgs(sys.argv[1:], data)
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
            for checker in data.checks:
                checkSolution(testfile, resfile, checker)
