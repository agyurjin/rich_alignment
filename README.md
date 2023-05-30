# Rich Alignment

## Tablle of content
 - [Introduction](#Introduction)
 - [Create geometry and optical files](#Create-geometry-and-optical-files)
 - [Run training](#Run-training)
 - [Find minima](#Find-minima)

## Introduction

The developed approch is to use Fast Monte Carlo (FastMC) RICH simulation output and find best RICH alignment parameters that describes reconstructed tracks.

## Create geometry and optical files

The input files for FastMC are geometry and optical files. To create data point the code example can be used

```
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


