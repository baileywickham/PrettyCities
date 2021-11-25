import requests
import sys
import re
import secretm
import csv
from typing import Union
import argparse



class GMaps:
    url: str = 'https://maps.googleapis.com/maps/api/streetview'

    def __init__(self, api_key : str, signature : str = None,
            size='180x180', pano=None ):
        self.api_key = api_key
        self.signature = signature
        self.size = size
        self.pano : str = pano

    def dmsToDec(self, coord: str) -> float:
        deg, minutes, seconds, direction =  re.split('''[°'"]''', coord)
        return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)

    def isDMS(self, maybeDMS: Union[str, float]) -> bool:
        if type(maybeDMS) == str:
            if "'" in maybeDMS or '"' in maybeDMS or '°' in maybeDMS:
                return True
        return False

    def getDMS(self, lat:str, long:str):
        lat : float = self.dmsToDec(lat)
        long : float = self.dmsToDec(long)
        return self.getDec(lat, long)

    def getDec(self, lat:str, long:str) -> requests.Response:
        params : dict[str, str] = {"size": self.size,
                'key' : self.api_key,
                'signature' : self.signature,
                'location': f'{lat},{long}'}
        r = requests.get(self.url, params=params)
        return r

    def getAndWriteToFile(self, lat:str, long:str):
        # assume lat and long are same format
        filename = '{lat[0:4]}-{long[0-4]}.jpg'
        if self.isDMS(lat):
            rsp = self.getDMS(lat, long)
        else:
            rsp = self.getDec(lat, long)
        if rsp.status_code != 200:
            print(f'error calling on {lat},{long}: {rsp.content}')
            return
        self.writeImageToFile(filename, rsp.content)



    def writeImageToFile(self, filename: str, data):
        with open(filename, 'wb') as f:
            f.write(data)


def parseFile(filename: str, gm: GMaps):
    with open(filename, 'r') as f:
        for line in f:
            lat, long = line.strip().split()
            gm.getAndWriteToFile(lat, long)

def runWithFile(filename:str):
    sm = secretm.Secrets()
    gm = GMaps(sm['api_key'])
    parseFile(filename, gm)

#lat, long = '''52°23'23.85"N   4°53'8.03"E'''.split()
if __name__ == "__main__":
    p = argparse.ArgumentParser('Google maps street view CLI')
    p.add_argument('--file')
    p.add_argument('--lat')
    p.add_argument('--long')
    args = p.parse_args()
    if args.file:
        runWithFile(args.file)

