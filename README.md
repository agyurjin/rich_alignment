# Rich Alignment

## Tablle of content
 - [Introduction](#Introduction)
 - [Input JSONs](#Input-jsons)
 - [Create geometry and optical files](#Create-geometry-and-optical-files)
 - [Run training](#Run-training)
 - [Find minima](#Find-minima)

## Introduction

The developed approch is to use Fast Monte Carlo (FastMC) RICH simulation or CLAS12 RICH reconstructed variation outputs and find best RICH alignment parameters that describes reconstructed tracks. The code provides functions to create geometry and optical files combinations to do reconstruction, train neural network model and find best RICH alignment parameters. 


## Input JSONs

There are 3 required input JSONs file to fully run the program. However, that doesn't mean that for all the functions the 3 files are requires. There files are 'keywords.json', 'training_config.json' and 'minima_config.json'.

1. 'keywords.json'

Template is in the repository jsons folder. Detailed images of each keyword structure is in keywords folder

### INPUT section

Consists of two parts `GEOMETRY` and `OPTICAL`. Both contains list of objects with mirrors and aerogel layers information. 

`GEOMETRY` contains information either from FastMC simulation or CLAS12 RICH variation reconstructed data alignment geometry files. Structure of each item is:

`OPTICAL` contaions information from FastMC simulation.

Each element has following structure.

`json
    [PARAMETER_RELATED_KEY]:{
        "exist": Should the parameter used in the training.,
        "grid": [MIN_VAL,MAX_VAL,POINT_NUM],
        "corr": [CORRELATED_PARAMETER_KEY]
        }
`

During data generation `grid` "MIN_VAL" and "MAX_VAL" range will be used.
For example "aerogel_b2_x" and "frontal_mirror_b2_x" are correlated it means if `corr` element was set the correlated value in the data file will have the same value. 

 
### OUTPUT

Consists of four parts `AEROGEL`, `TOPOLOGY`, `MAPMT` and `TRACKS`.

`AEROGEL` contains information from FastMC simulation reconstruction data.

`TOPOLOGY` contatins information from FastMC simulation reconstruction data.

`MAPMT` contains information either from FastMC simulation or CLAS12 RICH reconstruction data.

`TRACKS` contains information either from FastMC simulation or CLAS12 RICH reconstruction data.


`json
    [PARAMETER_RELATED_KEY]:{
        "exist": Should the parameter used in the training.,
        }
`

2. 'minima_config.json'

Configuration file to search best alignment parameters.

### MINIMA

`type`: Either "genetic" or "sgd"

`momentum`: Parameter for "sgd" ignore for "genetic" algorithm

`iters`: Number of iterations

`precisions`: Precision for each type physical values.

`number_of_samples`: Starting number of points.
    

3. 'training_config.json'

Configuration file for model training.

### META

File names to look for keywords in the dataset.

**Topology file namses area list as there are few possible topologies. Important to have all keywords related topology file names.**

### DATASETS

Path to positive and negative datasets. In each folder should be folders, where folder represents data point.

`neg_pos_mixing`: Either "average", "free" or "charge". 
"average" calculats output values as average of negative and positive values.
"free" uses negative and positive values as independant dimension.
"charge" creates data points for both negative and positive and adds charge information as "dummy" output dimension.

`charge`: Either "positive", "negative", "mixed". 
"positive" uses only positive data.
"negative" uses only negative data.
"mixed" used both data.

**IMPORTANT all possible combinations are not possible for those 2 parameters.**


### MODEL

Training model

`type`: "nn" neural network is only available.
`hidden_layer_neuroons`: Neural network structure

### TRAINING

`epochs`: Number of epochs
`optimizer`: Optimizer parameters
`norm`: Dataset normalization
`val_size`: Dataset split validation size
`batch_size`: Batch size for training
`shuffle`: Shuffle data before split


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


## Run training and find best alignment parameters

`run_sample.py` is code script to run training and find best alignment parameters

!!! IMPORTANT !!! change `trained_model_path` in the script.

`python3 run_sample.py` will run training and find best alignment parameters.

If the model is already trained it is possible to find only alignment parameters.

Comment line 8 and model will use trained model to find best alignment parameters.




