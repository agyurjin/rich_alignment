from pathlib import Path
import json
from src.data_handler import DataReader

jsons_path = Path('test')/'jsons'

def test_loaded_data_shapes():
    raw_keywords = json.load(open(jsons_path / 'keywords.json'))
    json_data = json.load(open(jsons_path / 'training_config.json'))
    
    json_data['DATASETS']['neg_pos_mixing'] = 'average'
    data_reader = DataReader(raw_keywords, json_data['META'], json_data['DATASETS'])
    x_train, x_val, y_train, y_val = data_reader.get_data()
    assert x_train.shape[1] == 4
    assert y_train.shape[1] == 5


    json_data['DATASETS']['neg_pos_mixing'] = 'free'
    data_reader = DataReader(raw_keywords, json_data['META'], json_data['DATASETS'])
    x_train, x_val, y_train, y_val = data_reader.get_data()
    assert x_train.shape[1] == 4
    assert y_train.shape[1] == 10
    
    json_data['DATASETS']['neg_pos_mixing'] = 'charge'
    data_reader = DataReader(raw_keywords, json_data['META'], json_data['DATASETS'])
    x_train, x_val, y_train, y_val = data_reader.get_data()
    assert x_train.shape[1] == 5
    assert y_train.shape[1] == 5
