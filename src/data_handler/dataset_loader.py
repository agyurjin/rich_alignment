'''
Dataset Loader
'''
from pathlib import Path
import torch
from ..file_handler import DataParser

class DatasetLoader():
    '''
    Dataset Loader object
    '''
    def __init__(self, dataset_path: Path, file_names: dict) -> None:
        '''
        Init method

        Parameters:
            dataset_path: Dataset directory path
            file_names: Names of the files from input metadata
        '''
        self.data_parser = DataParser()

        self.dataset_path = dataset_path
        self.file_names = file_names
        self.device='cpu'

    def get_next(self, folder_names: list, keywords: dict) -> tuple:
        '''
        With keywords get next batch from folder_names

        Parameters:
            folder_names: List of the folder names to make torch tensors
            keywords: keywords to use to make dataset

        Return:
            (dataset_x, dataset_y): (features, targets)
        '''
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

            top_data_dir = self.dataset_path / folder
            top_data = self._top_to_data(top_data_dir, self.file_names['top'], keywords['top'])

            dataset_x.append(geo_data+opt_data)
            dataset_y.append(aer_data+top_data)

        dataset_x = torch.tensor(dataset_x, dtype=torch.float, device=self.device)
        dataset_y = torch.tensor(dataset_y, dtype=torch.float, device=self.device)

        return dataset_x, dataset_y


    def _file_to_data(self, path, keywords):
        raw_data = self.data_parser.read_file(path)
        data = [raw_data[keyword] for keyword in keywords]
        return data



    def _top_to_data(self, fold_path, file_names, keywords):
        top_data_dict = {}
        for file_name in file_names:
            top_key = file_name.split('.')[2].split('_')[-1]
            top_data_dict = {}
            file_path = folder_path / file_name
            top_data_dict[top_key] = self.data_parser.read_file(file_path)

        data = []
        for keyword in keywords:
            top_key = keyword.split('_')[0]
            if top_key not in top_data_dict:
                print(f'File for {keyword} is not provided!. Skipping {keyword}!')
                continue

            data.append(top_data_dict[top_key][keyword])

        return data
                



