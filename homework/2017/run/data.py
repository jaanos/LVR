#!/usr/bin/env python

progs = {
    'Burek': 'run-Burek.sh',
    'CD': 'run-CD.sh',
    'Dobby': 'run-Dobby.sh',
    'Frimat': 'run-Frimat.sh',
    'FT': 'run-FT.sh',
    'IOLo': 'run-IOLo.sh',
    'JPV': 'run-JPV.sh',
    'KD': 'run-KD.sh',
    'KOE': 'run-KOE.sh',
    'LastMinuteSolution': 'run-LastMinuteSolution.sh',
    'Maaj': 'run-Maaj.sh',
    'mtsch': 'run-mtsch.sh',
    'muzik': 'run-muzik.sh',
    'Nesquik-boter': 'run-Nesquik-boter.sh',
    'pajaca': 'run-pajaca.sh',
    'Revcka': 'run-Revcka.sh',
    'shinySpork': 'run-shinySpork.sh',
    'SJN': 'run-SJN.sh',
    'slow-loris': 'run-slow-loris.sh',
    'Team2': 'run-Team2.sh',
}

checks = ['common/check-janos.py']

defaultTests = ['sudoku_mini.txt', 'sudoku_easy.txt', 'sudoku_hard.txt'] + \
               ['%s.txt' % team for team in sorted(progs.keys())]
