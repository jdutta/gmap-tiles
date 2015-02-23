# gmap-tiles
Script to import static google map tiles as images

## Motivation:
Build a high resolution static map image by stitching together smaller static map "tiles". Google static map api allows downloading 640x640 tiles, styled in a variety of ways. Those tiles can then be stitched manually in photoshop, or by some tool like hugin.

How to configure styling of static maps: play with https://snazzymaps.com/editor until desired style is obtainer, then from the json it is fairly straightforward to convert the config to the url params.

## config.json

#### url-template:
The static maps download url with variables `__LAT__`, `__LONG__` and `__ZOOM__` in place.

#### zoom:
The zoom factor. This will affect the following parameter.

#### increment:
The delta of latitude or longitude between successive tiles. First choose the zoom level, then play with the lat/long in url such that the next tile will have approx 20% overlap. The difference in latitude or longiture is the increment.

#### start-coord:
The lat/long of the top-left corner of the desired map.

#### end-coord:
The lat/long of the bottom-right corner of the desired map.

## Generate tiles:

Clear the `images` folder first.

`python ./generate_tiles.py`

This will generate the tiles in the `images` folder. The naming is: `tile-RR-CC.png` where `RR` is row index and `CC` is col index.
