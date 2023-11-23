from src import RICHAlignment
from pathlib import Path
import shutil

trained_model_path = '/home/agyurjin/infn/alignment/exp1/model9'

rich = RICHAlignment('jsons')
rich.run_training(trained_model_path)
rich.run_minimum_finder(trained_model_path)

