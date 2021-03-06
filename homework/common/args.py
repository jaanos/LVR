#!/usr/bin/env python

def parseArgs(args, data):
    setTeams, setTests = False, False
    listTeams, listTests = [], []
    activeTests = False
    for arg in args:
        if arg in ["--test", "--tests"]:
            setTests = True
            activeTests = True
        elif arg in ["--team", "--teams"]:
            setTeams = True
            activeTests = False
        elif activeTests:
            listTests.append(arg)
        else:
            setTeams = True
            listTeams.append(arg)
    if setTeams:
        teams = listTeams
    else:
        teams = sorted(data.progs.keys())
    if setTests:
        tests = ['%s.txt' % test for test in listTests]
    else:
        tests = data.defaultTests
    print('Teams: %s' % teams)
    print('Tests: %s' % tests)
    return (teams, tests)
