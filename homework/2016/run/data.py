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
    'strelec': 'run-strelec.sh',
    'sven': 'run-sven.sh',
    'team': 'run-team.sh'
}

checks = ['common/check-janos.py', 'check-3students.sh',
          'check-contradiction.py'] #, 'check-isrmjevci.sh']

defaultTests = ['sudoku1.txt', 'sudoku2.txt'] + \
               ['%s.txt' % team for team in sorted(progs.keys())]
