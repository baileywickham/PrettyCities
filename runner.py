from gMaps import *
import secretm
import csv
import argparse
from pathlib import Path

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
    lat, long = gm.convert(_lat, _long)
    gm.getAndWriteToFile(lat, long, filename)

def readCSV(filename: str, gm: GMaps, varyHeading):
    with open(filename, 'r') as f:
        c = csv.reader(f)
        for line in c:
            lat, long = gm.convert(line[0], line[1])
            if len(line) == 3:
                score = line[2]
            else:
                score=0

            fn = Filename(Path(filename).stem, score)
            gm.getAndWriteToFile(lat, long, fn, varyHeading=varyHeading,)


def runWithFile(filename:str, varyHeading=False, live=False):
    varyHeading = varyHeading if varyHeading else False
    dry_run = False if live else True
    sm = secretm.Secrets()
    gm = GMaps(sm['api_key'], dry_run=dry_run)
    readCSV(filename, gm, varyHeading )

if __name__ == "__main__":
    p = argparse.ArgumentParser('Google maps street view CLI')
    p.add_argument('--csv')
    p.add_argument('--lat')
    p.add_argument('--long')
    p.add_argument('--filter')
    p.add_argument('--varyHeading', action='store_true',  default=False)
    p.add_argument('--live', action='store_true',  default=False)
    args = p.parse_args()
    if args.csv:
        runWithFile(args.csv, varyHeading=args.varyHeading, live=args.live)
    elif args.lat and args.long:
        runWithCoord(args.lat, args.long)
    elif args.filter:
        filterFile(args.filter)
    else:
        p.print_help()
