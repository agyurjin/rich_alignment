'''
Main class to train different models
'''
import sys
from pathlib import Path
import numpy as np
import torch

from models.nn_model import NNModel
from models.poly_model import PolyModel

class Trainer():
    '''
    Class to create models and train
    '''
    def __init__(self, params=None):
        ''' Initialize trainer for model training

        Parameters:
            params (dict): Parameters for model creation and training

        Return:
            None
        '''
        configs = {}
        configs['epochs'] = params['TRAINING']['epochs']
        configs['lr'] = params['TRAINING']['optimizer']['lr']
        configs['momentum'] = params['TRAINING']['optimizer']['momentum']
        configs['norm'] = params['TRAINING']['norm']
        configs['net_structure'] = {
                                'input_layer': params['MODEL']['input_layer'],
                                'output_layer': params['MODEL']['output_layer'],
                                'hidden_layer_neurons': params['MODEL']['hidden_layer_neurons']
                                }
        if params['MODEL']['type'] == 'nn':
            self.model = NNModel(configs)
        elif params['MODEL']['type'] == 'poly':
            self.model = PolyModel(configs)
        else:
            print("ERROR: wrong model type! Should be one of the following ['nn', 'poly']! ")
            sys.exit()
        self.ratio = params['TRAINING']['split_ratio']
        self.output_path = Path(params['PATHS']['output_path'])

    def train_val_split(self, X, y):
        ''' Split data into train and validation set

        Parameters:
            X (torch.tensor): (N, F) dimensional features dataset
            y (torch.tensor): (N, T) dimensional target dataset

        Return:
            x_train (torch.tensor): (N', F) dimensional features tensor for trainset
            y_train (torch.tensor): (N', T) dimensional targets tensor for trainset
            x_val (torch.tensor): (N", F) dimensional features tensor for valset
            y_val (torch.tensor): (N", T) dimensional targets tensor for valset
        '''

        data = torch.hstack((X,y))
        N = int(data.size()[0] * self.ratio)
        data = data[torch.randperm(data.size()[0])]
        x_train = data[:N, :X.size()[1]]
        y_train = data[:N, X.size()[1]:]
        x_val = data[N:, :X.size()[1]]
        y_val = data[N:, X.size()[1]:]

        return x_train, y_train, x_val, y_val

    def only_1d_or_2d(self, x_train, y_train, x_val, y_val):
        '''
        Save train and validataion datas

        Parameters:
            x_train (torch.tensor): trainset features
            y_train (torch.tensor): trainset targets
            x_val (torch.tensor): validation features
            y_val (toch.tensor): validation targets
        '''
        dim = x_train.size()[1]
        np.save(str(self.output_path / 'trainset_x_{}d.npy'.format(dim)), x_train.numpy())
        np.save(str(self.output_path / 'trainset_y_{}d.npy'.format(dim)), y_train.numpy())
        np.save(str(self.output_path / 'valset_x_{}d.npy'.format(dim)), x_val.numpy())
        np.save(str(self.output_path / 'valset_y_{}d.npy'.format(dim)), y_val.numpy())

    def train(self, X, y):
        ''' Main function to train model

        Parameters:
            X (torch.tensor): (N, F) dimensional features dataset
            y (torch.tensor): (N, T) dimensional target dataset
        '''

        x_train, y_train, x_val, y_val = self.train_val_split(X, y)
        self.model.train(x_train, y_train, x_val, y_val)
        self.model.save_model(self.output_path / 'model.pth')

        if x_train.size()[1] < 3:
            self.only_1d_or_2d(x_train, y_train, x_val, y_val)
