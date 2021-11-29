# PrettyCities
Characterize and generate pretty cities

[Street view API](https://developers.google.com/maps/documentation/streetview/overview)

## Use
Requries `pipenv` and `python3.9`. Use `pipenv install` to install dependencies.

Use `runner.py` provides the google maps API as well as filter helpers. 

The [jupyter notebook](/PrettyCities.ipynb) contains the model, the `gMaps.py` file contians a wrapper around the google maps street view API to fetch photos. 


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
g.getAndWriteToFile(lat, long, filename, varyCoord=False, varyHeading=False)
```

### Filename
The filename class generates a unique filename for each file. It takes a base name and generates unique file names. 
