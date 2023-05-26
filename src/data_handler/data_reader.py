'''
Data Loader
'''
from pathlib import Path
import random
from sklearn.model_selection import train_test_split
import torch

from .dataset_reader import DatasetReader

class DataReader():
    '''
    Data Loader object
    '''
    def __init__(self, raw_keywords: dict, metadata: dict, dataset_info: dict) -> None:
        '''
        Create data loader object

        Parameters:
            raw_keywords: keywords information from JSON file
            metadata: Paths and file names
            dataset_info: Dataset handeling information
        '''
        self.in_dim = None
        self.out_dim = None

        def keywords_reader(keywords):
            return [key for keyword in keywords for key, values in keyword.items() \
if values["exists"]]

        self.mixing = dataset_info['neg_pos_mixing']

        self.keywords = {
            'geo': keywords_reader(raw_keywords['INPUT']['GEOMETRY']),
            'opt': keywords_reader(raw_keywords['INPUT']['OPTICAL']),
            'aer': keywords_reader(raw_keywords['OUTPUT']['AEROGEL']),
            'top': keywords_reader(raw_keywords['OUTPUT']['TOPOLOGY'])
        }

        self.in_dim = len(self.keywords['geo']) + len(self.keywords['opt'])
        self.out_dim = len(self.keywords['aer']) + len(self.keywords['top'])
        if dataset_info['charge'] == 'mixed':
            if self.mixing == 'charge':
                self.in_dim += 1
            elif self.mixing == 'free':
                self.out_dim *= 2

        neg_file_names = {
            'geo': metadata['geometry_file_name'],
            'opt': metadata['optical_file_name'],
            'aer': metadata['aerogel_neg_part_file_name'],
            'top': metadata['topology_neg_part_file_names']
        }

        pos_file_names = {
            'geo': metadata['geometry_file_name'],
            'opt': metadata['optical_file_name'],
            'aer': metadata['aerogel_pos_part_file_name'],
            'top': metadata['topology_pos_part_file_names']
        }

        self.neg_dataset_reader, self.pos_dataset_reader = None, None
        neg_part_dataset_path = Path(dataset_info['neg_part_dataset_path'])
        pos_part_dataset_path = Path(dataset_info['pos_part_dataset_path'])

        if dataset_info['charge'] == 'mixed':
            self.neg_dataset_reader = DatasetReader(neg_part_dataset_path, neg_file_names)
            self.pos_dataset_reader = DatasetReader(pos_part_dataset_path, pos_file_names)
        elif dataset_info['charge'] == 'positive':
            self.pos_dataset_reader = DatasetReader(pos_part_dataset_path, pos_file_names)
        elif dataset_info['charge'] == 'negative':
            self.neg_dataset_reader = DatasetReader(neg_part_dataset_path, neg_file_names)
#            print('ERROR: charge should be one of this ["mixed", "positive", "negative"]!')

        iterable_folder = dataset_info['neg_part_dataset_path'] 
        if dataset_info['charge'] == 'positive':
            iterable_folder = dataset_info['pos_part_dataset_path']

        self.dataset_folder_names = []
        for folder_path in Path(iterable_folder).iterdir():
            if folder_path.is_file():
                continue
            self.dataset_folder_names.append(folder_path.name)


    def get_data(self, test_size=0.2):
        x, y = self._preprocess_set(self.dataset_folder_names)
        x_train, y_train, x_val , y_val = train_test_split(x,y, test_size=test_size)
        return x_train, y_train, x_val, y_val


    def _preprocess_set(self, dataset:list) -> tuple:
        '''
        Convert files to torch tensors preprocess data with
        charge and mixing

        Parameters:
            dataset: List of data points folder path
        Return:
            (x, y): Dataset (features,targets)
        '''
        pos_x, pos_y = None, None
        if self.pos_dataset_reader:
            pos_x, pos_y = self.pos_dataset_reader.read_dataset(dataset, self.keywords)

        neg_x, neg_y = None, None
        if self.neg_dataset_reader:
            neg_x, neg_y = self.neg_dataset_reader.read_dataset(dataset, self.keywords)

        if self.mixing == 'average':
            x = (neg_x + pos_x)/2
            y = (neg_y + pos_y)/2
        elif self.mixing == 'free':
            x = neg_x
            y = torch.hstack((neg_y, pos_y))
        elif self.mixing == 'charge':
            x = torch.vstack((neg_x, pos_x))
            N = len(dataset)
            c = torch.hstack((torch.zeros(N), torch.ones(N))).reshape((2*N,1))
            x = torch.hstack((x,c))
            y = torch.vstack((neg_y, pos_y))

        return x, y
