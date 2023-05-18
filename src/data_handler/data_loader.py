'''
'''
import json
from pathlib import Path
import torch
import random

from .dataset_loader import DatasetLoader

class DataLoader():
    def __init__(self, raw_keywords: dict, metadata: dict, dataset_info: dict) -> None:
        self.batch_id = 0
        self.trainset = None
        self.len_testset = None
        self.in_dim = None
        self.out_dim = None

        def keywords_reader(keywords):
            return [key for keyword in keywords for key, values in keyword.items() if values["exists"]]

        self.mixing = dataset_info['neg_pos_mixing']
        self.charge =  dataset_info['charge']
        
        self.keywords = {
            'geo': keywords_reader(raw_keywords['INPUT']['GEOMETRY']),
            'opt': keywords_reader(raw_keywords['INPUT']['OPTICAL']),
            'aer': keywords_reader(raw_keywords['OUTPUT']['AEROGEL']),
            'top': keywords_reader(raw_keywords['OUTPUT']['TOPOLOGY'])
        }

        self.in_dim = len(self.keywords['geo']) + len(self.keywords['opt'])
        self.out_dim = len(self.keywords['aer']) + len(self.keywords['top'])
        if self.charge == 'mixed':
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

        self.neg_dataset_loader, self.pos_dataset_loader = None, None
        if self.charge == 'mixed':
            self.neg_dataset_loader = DatasetLoader(Path(dataset_info['neg_part_dataset_path']), neg_file_names)
            self.pos_dataset_loader = DatasetLoader(Path(dataset_info['pos_part_dataset_path']), pos_file_names)
        elif self.charge == 'positive':
            self.pos_dataset_loader = DatasetLoader(Path(dataset_info['pos_part_dataset_path']), pos_file_names)
        elif self.charge == 'negative':
            self.neg_dataset_loader = DatasetLoader(Path(dataset_info['neg_part_dataset_path']), neg_file_names)
        else:
            print('ERROR: charge should be one of this ["mixed", "positive", "negative"]!')

        iterable_folder = dataset_info['pos_part_dataset_path'] if self.charge == 'positive' else dataset_info['neg_part_dataset_path']
      
        self.dataset_folder_names = []
        for folder_path in Path(iterable_folder).iterdir():
            if folder_path.is_file():
                continue
            self.dataset_folder_names.append(folder_path.name)

    def split_data(self, split_ratio, batch_size, shuffle=True):
        if shuffle:
            random.shuffle(self.dataset_folder_names)
        
        N = int(len(self.dataset_folder_names)*split_ratio)
        self.trainset = self.dataset_folder_names[:N]
#        last_batch = 1 if N%batch_size != 0 else 0
#        self.num_of_batches = N//batch_size + last_batch
#        self.batched_trainset = [self.trainset[i*batch_size:(i+1)*batch_size] for i in range(self.num_of_batches)]
        self.testset = self.dataset_folder_names[N:]
        self.len_trainset, self.len_testset =  len(self.trainset), len(self.testset)
#        self.num_of_batches = len(self.batched_trainset)
        

#    def get_next_batch(self):
#        x, y = self._preprocess_set(self.batched_trainset[self.batch_id])
#        self.batch_id = (self.batch_id + 1) % self.num_of_batches
#        return x, y
    def get_trainset(self):
        x, y = self._preprocess_set(self.trainset)
        return x, y

    def get_testset(self):
        x, y = self._preprocess_set(self.testset)
        return x, y

    def _preprocess_set(self, dataset):
        x, y = None, None
        if self.charge == 'positive':
            x, y = self.pos_dataset_loader.get_next(dataset, self.keywords)
        elif self.charge == 'negative':
            x, y = self.neg_dataset_loader.get_next(dataset, self.keywords)
        elif self.charge == 'mixed':
            neg_x, neg_y = self.neg_dataset_loader.get_next(dataset, self.keywords)
            pos_x, pos_y = self.pos_dataset_loader.get_next(dataset, self.keywords)
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
 #               self.mean.apppend(0)
 #               self.std.append(1)

        return x, y
