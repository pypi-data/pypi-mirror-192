# `aircraft_models` Documentation

## Installation

Installation is easy using `pip` and will install all required
libraries.

```bash
$ pip install aircraft-list
```

## How to use aircraft_list

```python
from aircraft_list import aircraft_models

aircrafts = aircraft_models()


```

It returns a list of dictionaries which can be addressed as follows:

```python
for ac in aircrafts:
    ac['manufacturer'] #it returns the aircraft manufacturer
    ac['model'] #it returns the aircraft model
    ac['icao'] #it returns the icao_code designator
    ac['type'] #it returns the aircraft type
    ac['engine'] #it returns the aircraft engine type
    ac['engine_number'] #it returns the aircraft engine number
    ac['wake'] #it returns the aircraft wake turbulence category
```

The list of dictionary is updated as per ICAO DOC 8643 - Aircraft Type Designator
