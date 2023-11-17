# Rich Alignment

## Tablle of content
 - [Introduction](#Introduction)
 - [Input JSONs](#Input-jsons)
 - [Create geometry and optical files](#Create-geometry-and-optical-files)
 - [Run training](#Run-training)
 - [Find minima](#Find-minima)

## Introduction

The developed approch is to use Fast Monte Carlo (FastMC) RICH simulation output and find best RICH alignment parameters that describes reconstructed tracks. The code provides functions to create geometry and optical files combinations to do reconstruction, train neural network model with FastMC reconstruction output and find minima, which is best set of parameters that produce best results for the reconstructed chi-square topolpgies. 

## Input JSONs

There are 3 required input JSONs file to fully run the program. However, that doesn't mean that for all the functions the 3 files are requires. There files are 'keywords.json', 'training_config.json' and 'minima_config.json'.

1. 'keywords.json'

Template is in the repository jsons folder.

### INPUT section

Consists of two parts `GEOMETRY` and `OPTICAL`. Both contains list of objects with mirrors and aerogel layers information. 

`GEOMETRY` object is a list of elements that contain information either from FastMC simulation or from real data alignment variance file. Structure of each item is:

`json

    [PARAMETER_RELATED_KEY]:{
        "exist": Should the parameter used in the training.,
        "grid": [MIN_VAL,MAX_VAL,POINT_NUM],
        "corr": [CORRELATED_PARAMETER_KEY]
        }
`

During data generation `grid` "MIN_VAL" and "MAX_VAL" range will be used.
For example "aerogel_b2_x" and "frontal_mirror_b2_x" are correlated it means if `corr` element was set the correlated value in the data file will have the same value. 

`OPTICAL` object is the
 
### OUTPUT

Consists of four parts `AEROGEL`, `TOPOLOGY`, `MAPMT` and `TRACKS`. 


2. 'training_config.json'



3. 'minima_config.json'

Configuration file to search best alignment parameters.
 

## Create geometry and optical files

The input files for FastMC are geometry and optical files. To create data point the code example can be used

```python3
from src import RICHAlignment

input_jsons = 'jsons' # path to input jsons
output_path = 'output' # path to output folder (folder will created if not exists)
num_of_points = 100 # number of points to create
geo_path = 'templates/RichModGeometry.dat' # path to geometry file template
opt_path = 'templates/RichModOptical.dat' # path to optical file template

rich = RICHAlignment(input_jsons)
rich.create_data(output_path, num_of_points, geo_path, opt_path)
```


## Run training

## Find minima


