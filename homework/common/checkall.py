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

def run(data, minsize = None):
    teams, tests = parseArgs(sys.argv[1:], data)
    for test in tests:
        testfile = '../dimacs/%s' % test
        for team in teams:
            resfile = 'results/%s_%s' % (team, test)
            try:
                stat = os.stat(resfile)
                if minsize is not None and stat.st_size <= minsize:
                    continue
            except OSError:
                continue
            print('\n=====================================')
            print('\nChecking the solution to %s by %s ...' % (test, team))
            sys.stdout.flush()
            for checker in data.checks:
                checkSolution(testfile, resfile, checker)
