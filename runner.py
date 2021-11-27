from gMaps import *
import secretm
import csv
import argparse

def filterFile(filename):
    with open(filename, 'r') as f, open(filename + '.csv', 'w') as o:
        w = csv.writer(o)
        for line in f:
            if line.strip() != '':
                w.writerow(line.split())

def runWithCoord(_lat:str, _long:str):
    sm = secretm.Secrets()
    gm = GMaps(sm['api_key'])
    filename = Filename('{lat[0:3]}-{long[0:3]}')
    lat, long = gm.contvert(_lat, _long)
    gm.getAndWriteToFile(lat, long, filename)

def readCSV(filename: str, gm: GMaps):
    with open(filename, 'r') as f:
        c = csv.reader(f)
        for line in c:
            lat, long = gm.contvert(line[0], line[1])
            if len(line) == 3:
                score = line[3]
            else:
                score=0
            fn = Filename(filename, score)
            gm.getAndWriteToFile(lat, long, fn)


def runWithFile(filename:str):
    sm = secretm.Secrets()
    gm = GMaps(sm['api_key'])
    readCSV(filename, gm)

if __name__ == "__main__":
    p = argparse.ArgumentParser('Google maps street view CLI')
    p.add_argument('--csv')
    p.add_argument('--lat')
    p.add_argument('--long')
    p.add_argument('--filter')
    args = p.parse_args()
    if args.csv:
        runWithFile(args.csv)
    if args.lat and args.long:
        runWithCoord(args.lat, args.long)
    if args.filter:
        filterFile(args.filter)

    else:
        p.print_help()
