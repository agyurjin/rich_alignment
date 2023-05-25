from pathlib import Path
import json
from src.data_handler import DataLoader

jsons_path = Path('test')/'jsons'

def test_loaded_data_shapes():
    raw_keywords = json.load(open(jsons_path / 'keywords.json'))
    json_data = json.load(open(jsons_path / 'training_config.json'))
    
    json_data['DATASETS']['neg_pos_mixing'] = 'average'
    data_loader = DataLoader(raw_keywords, json_data['META'], json_data['DATASETS'])
    data_loader.split_data(0.8, 7)
    x, y = data_loader.get_next()
    assert x.shape == (7, 4)
    assert y.shape == (7, 5)


    json_data['DATASETS']['neg_pos_mixing'] = 'free'
    data_loader = DataLoader(json_data['META'], json_data['DATASETS'])
    data_loader.split_data(0.8, 7)
    x, y = data_loader.get_next()
    assert x.shape == (7, 4)
    assert y.shape == (7, 10)
    
    json_data['DATASETS']['neg_pos_mixing'] = 'charge'
    data_loader = DataLoader(json_data['META'], json_data['DATASETS'])
    data_loader.split_data(0.8, 7)
    x, y = data_loader.get_next()
    assert x.shape == (14, 5)
    assert y.shape == (14, 5)
