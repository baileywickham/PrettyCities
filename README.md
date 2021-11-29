# PrettyCities
Characterize and generate pretty cities

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/baileywickham/PrettyCities/blob/main/PrettyCities.ipynb)


[Street view API](https://developers.google.com/maps/documentation/streetview/overview)

Given a set of street view images of a city deemed pretty (0-9 scale), train a model on this score. The biggest problem with this is data, all labels are hand generated. Even using tricks like varying heading reduces the accuracy of the labels. 

## Use
Requries `pipenv` and `python3.9`. Use `pipenv install` to install dependencies.

The [jupyter notebook](/PrettyCities.ipynb) contains the model, the `gMaps.py` file contians a wrapper around the google maps street view API to fetch photos. 

Use `runner.py` provides the google maps API as well as filter helpers:
```python
usage: Google maps street view CLI [-h] [--csv CSV] [--lat LAT] [--long LONG] [--filter FILTER] [--varyHeading]
                                   [--live]

optional arguments:
  -h, --help       show this help message and exit
  --csv CSV        Take input of <lat,long,score> from csv, download each image and write to a file
  --lat LAT        Use with long, download one file
  --long LONG      Use with lat, download one file
  --filter FILTER  filter a file from the speadsheet into a CSV
  --varyHeading    vary the heading on the images, use default, 0, 90, 180, 270
  --live           turn off dry_run
```

## gMaps
`gMaps.py` provides a basic google maps street view API. 

Init the module
```python
g = GMaps('api-key', dry_run=False)
```
### API:

Convert DMS to dec, leaves coordinates unchanged if passed in as decimal. 
```python
lat, long = g.convert(coordinates...)
```

Get a streetview and write the jpg to a file. if `varyHeading` is set, 5 images will be downloaded: default heading, then 0, 90, 180, 270 degrees. 
```python
g.getAndWriteToFile(lat, long, Filename(basename), varyCoord=False, varyHeading=False)
```

### Filename
The filename class generates a unique filename for each file. It takes a base name and generates unique file names. 

Given a base name `city` and a score of `5`, this will be written `data/5/5-city-xxxxxx.jpg` where the `x`s are random ints. 
