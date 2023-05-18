from src import RICHAlignment
from pathlib import Path

folder_names = ['model_17_05_m_5d', 'model_17_05_m_dp', 'model_17_05_m_s5c_b1', 'model_17_05_m_s5c_b2']


trained_model_path = str(Path('/home/agyurjin/infn/infn_nn')/'test_new_v1')
rich = RICHAlignment('jsons')
rich.run_training(trained_model_path)
rich.run_prediction(trained_model_path)
