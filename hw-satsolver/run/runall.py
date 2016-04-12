#!/usr/bin/env python

import os
import time
import csv
import subprocess
import select
import fcntl
import signal

progs = {
    '3students': 'run-3students.sh',
    'memo': 'run-memo.py',
    'team': 'run-team.sh',
    'achtung': 'run-achtung.sh',
    'salt-n-pepa': 'run-salt-n-pepa.py',
    'isrmjevci': 'run-isrmjevci.py',
    'sven': 'run-sven.sh',
    'sml': 'run-sml.py',
    'contradiction': 'run-contradiction.py',
    'biblethump': 'run-biblethump.py',
    'goodboy': 'run-goodboy.py',
    'duzl-studios': 'run-duzl-studios.sh',
    'pythonsolver': 'run-pythonsolver.py'
}

teams = sorted(progs.keys())
tests = ['sudoku1.txt', 'sudoku2.txt'] + ['%s.txt' % team for team in teams]

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

def runTests(ts):
    times = {}
    for test in ts:
        times[test] = {}
        for team in teams:
            times[test][team] = testSolver(team, test)
    return times

def writeResults(times):
    ts = times.keys()
    tab = [[''] + ts] + \
          [[team] + [times[test][team] if team in times[test] else ''
                     for test in ts] for team in teams]
    with open('results/times-%s.csv' % time.strftime('%Y-%m-%d_%H%M%S'),
              'w') as f:
        csv.writer(f).writerows(tab)

if __name__ == '__main__':
    for test in tests:
        times = runTests([test])
        writeResults(times)
