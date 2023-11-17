from src import RICHAlignment
from pathlib import Path
import shutil

trained_model_path_main = '/home/agyurjin/infn/alignment/exp1/model9'

rich = RICHAlignment('jsons')
rich.run_training(trained_model_path_main)
rich.run_minimum_finder(trained_model_path_main)

#for i in range(10000, 101000, 10000):
#    trained_model_path = f'./model_{i}'
#    rich = RICHAlignment('jsons')
#    shutil.copy(f'{trained_model_path_main}/training_config.json', f'{trained_model_path}/training_config.json')
#    rich.run_minimum_finder(trained_model_path)

