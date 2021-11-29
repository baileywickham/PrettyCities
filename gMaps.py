import requests
import re
from typing import Union, Optional, cast

import random
import string

datadir = 'data'

class Filename():
    def __init__(self, base, score=0) -> None:
        self.base = base
        self.score = score
    def setScore(self, score):
        self.score = score

    def genID(self, len=6):
        return ''.join(random.choice(string.digits) for _ in range(len))

    def build(self):
        return f'{datadir}/{self.score}/{self.buildFilename()}'

    def buildFilename(self):
        return f'{self.score}-{self.base}-{self.genID()}.jpg'
    def buildWithHeading(self, heading:Union[str,float]):
        return f'{datadir}/{self.score}/{self.score if self.score else 0}-{self.base}-{heading}-{self.genID()}.jpg'



class GMaps:
    url: str = 'https://maps.googleapis.com/maps/api/streetview'

    def __init__(self, api_key : str, signature:str=None,
            size='180x180', pano:str=None, dry_run=True):
        self.api_key = api_key
        self.signature = signature
        self.size = size
        self.pano : Optional[str] = pano
        self.dry_run : bool = dry_run

    def convert(self, *args) -> list[float]:
        converted = []
        for arg in args:
            if self.isDMS(arg):
                converted.append(self.dmsToDec(arg))
            else:
                converted.append(arg)
        return converted

    def dmsToDec(self, *args) -> Union[float, list[float]]:
        converted = []
        for arg in args:
            deg, minutes, seconds, direction =  re.split('''[°'"]''', arg)
            converted.append((float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1))
        if len(converted) == 1:
            return converted[0]
        return converted

    def isDMS(self, maybeDMS: Union[str, float]) -> bool:
        if isinstance(maybeDMS, str):
            if "'" in maybeDMS and '"' in maybeDMS and '°' in maybeDMS:
                return True
        return False

    def get(self, params:dict[str,Union[str,float,None]]) -> Optional[requests.Response]:
        params['key'] = self.api_key
        params['signature'] = self.signature
        params['source'] = 'outdoor'
        if self.dry_run:
            print(requests.Request('GET', self.url, params=params).prepare().path_url)
        else:
            rsp = requests.get(self.url, params=params)
            setattr(rsp, 'params', params)
            return rsp

    def getAndWriteToFile(self, lat:float, long:float, filename:Filename,
            varyHeading=False,
            varyCoord=False):
        params = {'size':self.size,
                'location': f'{lat},{long}'}

        requestsWithFilenames = [(params, filename.build())]
        if varyHeading:
            requestsWithFilenames += [(params | {'heading':x}, filename.buildWithHeading(x)) for x in [0, 90, 190, 270]]
        responses = [(self.get(r), f) for r,f in requestsWithFilenames]

        for r, name in responses:
            if r == None:
                print(f'Response for filename {name}')
                return
            if r.ok:
                self.writeImageToFile(name, r.content)
            else:
                print(f'error calling on {lat},{long}: {r.content}')

    def writeImageToFile(self, filename: str, data):
        print(f'writing {filename}')
        with open(filename, 'wb') as f:
            f.write(data)
