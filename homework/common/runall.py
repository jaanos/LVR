#!/usr/bin/env python

import os
import sys
import time
import csv
import subprocess
import select
import fcntl
import signal

from data import progs
from args import parseArgs

def testSolver(team, test, poll = 1, timeout = 600, maxread = 1024):
    print('\n=====================================')
    print('\nRunning %s on %s ...' % (team, test))
    out = ''
    p = subprocess.Popen(['/usr/bin/time', '-f', '%e', './%s' % progs[team],
                          '../dimacs/%s' % test, 'results/%s_%s' % (team, test)],
                          stderr = subprocess.PIPE, preexec_fn = os.setsid)
    flags = fcntl.fcntl(p.stderr, fcntl.F_GETFL)
    if not p.stderr.closed:
        fcntl.fcntl(p.stderr, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    try:
        r = None
        while r != '':
            r = p.stderr.read(maxread)
            out += r
    except IOError:
        pass
    finally:
        ret = p.poll()
    s, m, ms = 0, 0, 0
    while ret is None:
        if s > timeout:
            print('Timeout of %d seconds exceeded' % timeout)
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
            return
        time.sleep(poll)
        s += poll
        ms += poll
        if ms >= 60:
            m += ms//60
            ms %= 60
            print('%d minutes passed...' % m)
        try:
            r = None
            while r != '':
                r = p.stderr.read(maxread)
                out += r
        except IOError:
            pass
        finally:
            ret = p.poll()
    print('Exited with code %d' % ret)
    try:
        t = float(out.split()[-1])
        print('Time elapsed: %.3f s' % t)
        return t
    except IndexError:
        print('Error fetching time; rough estimate: %d s' % s)
        return s

def runTests(ts, teams):
    times = {}
    for test in ts:
        times[test] = {}
        for team in teams:
            times[test][team] = testSolver(team, test)
    return times

def writeResults(times, teams):
    ts = times.keys()
    tab = [[''] + ts] + \
          [[team] + [times[test][team] if team in times[test] else ''
                     for test in ts] for team in teams]
    with open('results/times-%s.csv' % time.strftime('%Y-%m-%d_%H%M%S'),
              'w') as f:
        csv.writer(f).writerows(tab)

if __name__ == '__main__':
    teams, tests = parseArgs(sys.argv[1:])
    for test in tests:
        times = runTests([test], teams)
        writeResults(times, teams)
