#!/usr/bin/env python3
import csv
import sys

def cleanFile(filename):
    with open(filename, 'r') as f, open(filename + '.csv', 'w') as o:
        w = csv.writer(o)
        for line in f:
            if line.strip() != '':
                w.writerow(line.split())

cleanFile(sys.argv[1])
