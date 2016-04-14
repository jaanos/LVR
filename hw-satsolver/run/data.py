#!/usr/bin/env python

progs = {
    '3students': 'run-3students.sh',
    'achtung': 'run-achtung.sh',
    'biblethump': 'run-biblethump.py',
    'contradiction': 'run-contradiction.py',
    'duzl-studios': 'run-duzl-studios.sh',
    'goodboy': 'run-goodboy.py',
    'isrmjevci': 'run-isrmjevci.py',
    'memo': 'run-memo.py',
    'pythonsolver': 'run-pythonsolver.py',
    'salt-n-pepa': 'run-salt-n-pepa.py',
    'sml': 'run-sml.sh',
    'sven': 'run-sven.sh',
    'team': 'run-team.sh'
}

checks = ['check-janos.py', 'check-3students.sh',
          'check-contradiction.py'] #, 'check-isrmjevci.sh']

tests = ['sudoku1.txt', 'sudoku2.txt'] + \
        ['%s.txt' % team for team in sorted(progs.keys())]
