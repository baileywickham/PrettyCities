import requests
import re
import secretm
import argparse
from typing import Union, Optional

import random
import string


class GMaps:
    url: str = 'https://maps.googleapis.com/maps/api/streetview'

    def __init__(self, api_key : str, signature:str=None,
            size='180x180', pano:str=None ):
        self.api_key = api_key
        self.signature = signature
        self.size = size
        self.pano : Optional[str] = pano

    def dmsToDec(self, coord: str) -> float:
        deg, minutes, seconds, direction =  re.split('''[°'"]''', coord)
        return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)

    def isDMS(self, maybeDMS: Union[str, float]) -> bool:
        if isinstance(maybeDMS, str):
            if "'" in maybeDMS or '"' in maybeDMS or '°' in maybeDMS:
                return True
        return False

    def get(self, params:dict[str,Union[str,float,None]]) -> requests.Response:
        params['key'] = self.api_key
        params['signature'] = self.signature
        params['source'] = 'outdoor'
        return requests.get(self.url, params=params)

    def getDMS(self, _lat:str, _long:str):
        lat : float = self.dmsToDec(_lat)
        long : float = self.dmsToDec(_long)
        return self.getDec(lat, long)

    def getDec(self, lat:Union[str, float], long:Union[str, float]) -> requests.Response:
        params : dict[str, Union[str, None, float]] = {
                'size': self.size,
                'location': f'{lat},{long}',}
        return self.get(params)

    def getAndWriteToFile(self, lat:str, long:str, filename:str):
        # assume lat and long are same format
        #filename = '{lat[0:4]}-{long[0-4]}.jpg'
        if self.isDMS(lat):
            rsp = self.getDMS(lat, long)
        else:
            rsp = self.getDec(lat, long)
        if rsp.status_code != 200:
            print(f'error calling on {lat},{long}: {rsp.content}')
        else:
            self.writeImageToFile(filename, rsp.content)

    def writeImageToFile(self, filename: str, data):
        print(f'writing {filename}')
        with open(filename, 'wb') as f:
            f.write(data)

    def getAndVarryHeading(self, lat:str, long:str):
        params = {'lat':lat, 'long':long}
        # type checker is wrong here, need to cast
        return [self.get(p) for p in [params | {'heading':x} for x in [None, 0, 90, 190, 270]]]

def runFromFile(filename: str, gm: GMaps):
    with open(filename, 'r') as f:
        for line in f:
            score = 5
            lat, long = line.strip().split()
            num = ''.join(random.choice(string.digits) for i in range(4))
            fn = f'data/{score}-{filename}-{num}.jpg'
            gm.getAndWriteToFile(lat, long, fn)

def runWithFile(filename:str):
    sm = secretm.Secrets()
    gm = GMaps(sm['api_key'])
    runFromFile(filename, gm)

def runWithCoord(lat:str, long:str):
    sm = secretm.Secrets()
    gm = GMaps(sm['api_key'])
    filename = '{lat[0:3]}-{long[0:3]}.jpg'
    gm.getAndWriteToFile(lat, long, filename)


#lat, long = '''52°23'23.85"N   4°53'8.03"E'''.split()
if __name__ == "__main__":
    p = argparse.ArgumentParser('Google maps street view CLI')
    p.add_argument('--file')
    p.add_argument('--lat')
    p.add_argument('--long')
    args = p.parse_args()
    if args.file:
        runWithFile(args.file)
    if args.lat and args.long:
        runWithCoord(args.lat, args.long)

