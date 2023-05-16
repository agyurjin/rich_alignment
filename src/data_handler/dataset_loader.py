import json
import torch

from ..file_handler import DataParser

class DatasetLoader():
    def __init__(self, dataset_path, file_names):
        self.data_parser = DataParser()

        self.dataset_path = dataset_path
        self.file_names = file_names
        self.device='cpu'
    
    def get_next(self, folder_names, keywords):
#        top_path: TODO implement 
        dataset_x = []
        dataset_y = []
        for folder in folder_names:
            geo_data_path = self.dataset_path / folder / self.file_names['geo']
            geo_data = self._file_to_data(geo_data_path, keywords['geo'])

            opt_data_path = self.dataset_path / folder / self.file_names['opt']
            opt_data = self._file_to_data(opt_data_path, keywords['opt'])
            
            aer_data_path = self.dataset_path / folder / self.file_names['aer']
            aer_data = self._file_to_data(aer_data_path, keywords['aer'])

            dataset_x.append(geo_data+opt_data)
            dataset_y.append(aer_data)

        dataset_x = torch.tensor(dataset_x, dtype=torch.float, device=self.device)
        dataset_y = torch.tensor(dataset_y, dtype=torch.float, device=self.device)
    
        return dataset_x, dataset_y


    def _file_to_data(self, path, keywords):
        raw_data = self.data_parser.read_file(path)
        data = [raw_data[keyword] for keyword in keywords]
        return data


