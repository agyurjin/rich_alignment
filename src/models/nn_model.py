'''
NN model
'''
import sys
import json
from pathlib import Path

import torch

from .base_model import BaseModel
from .nets import fcn

class NNModel(BaseModel):
    '''
    Neural Network model class
    '''
    def __init__(self, configs):
        '''
        Create object with configs

        Parameters:
            configs (dict): Configs to create model, training values

        Return:
            None
        '''
        super().__init__()
        self.lr = configs['lr']
        self.epochs = configs['epochs']
        self.momentum = configs['momentum']
        self.norm = configs['norm']

        if 'net_structure' not in configs:
            print("ERROR: 'net_structure' key doesn't exist in configs to create model")
            sys.exit()

        self.net_structure = configs['net_structure']
        self.model = fcn(self.net_structure)

    def train(self, x_train, y_train, x_val, y_val):
        '''
        Train model and keep best on validation set

        Parameters:
            x_train: (N', F) dimensional tensor for training features
            y_train: (N', T) dimensional tensor for training targets
            x_val: (N", F) dimensional tensor for validation features
            y_val: (N", T) dimensional tensor for validation targets

        Return :
            None
        '''

        x_train, y_train = self._preprocess_data(x_train, y_train, True)
        x_val, y_val = self._preprocess_data(x_val, y_val, False)

        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr, momentum=self.momentum)
        loss_fn = torch.nn.MSELoss()
        running_loss = 0
        best_model = None
        best_loss = 1e10
        for i in range(self.epochs):
            for x,y in zip(x_train, y_train):
                optimizer.zero_grad()
                y_pred = self.model(x)
                loss_v = loss_fn(y, y_pred)
                loss_v.backward()
                optimizer.step()
                running_loss += float(loss_v)
            if (i+1) % 1000 == 0:
                val_loss = 0
                with torch.no_grad():
                    for x_v, y_v in zip(x_val, y_val):
                        y_pred = self.model(x_v)
                        loss_v = loss_fn(y_v, y_pred)
                        val_loss += float(loss_v)
                if val_loss < best_loss:
                    best_model = self.model
                    best_loss = val_loss

                print('*'*20)
                print('[TRAINING] Epoch {}/{}'.format(i+1, self.epochs))
                print('[TRAINING] train loss: {:.5}'.format(running_loss/1000))
                print('[TRAINING] val loss: {:.5}'.format(val_loss/len(y_val)))
                print('*'*20)
                running_loss = 0

        if self.epochs < 1000:
            best_model = self.model

        self.model = best_model

    def _save_configs(self, output_path):
        '''
        Save config information for the training

        Parameters:
            output_path (Path or str): Output path
        '''
        folder_name = output_path.parent
        file_name = '{}_configs.json'.format(output_path.stem)
        configs = {
            'lr': self.lr,
            'momentum': self.momentum,
            'net_structure': self.net_structure,
            'norm': {
                'x_means' : self.data_means[:self.feature_size].tolist(),
                'x_stds' : self.data_stds[:self.feature_size].tolist(),
                'y_means' : self.data_means[self.feature_size:].tolist(),
                'y_stds' : self.data_stds[self.feature_size:].tolist()
            }
        }

        with open(str(folder_name/file_name), 'w') as fw:
            json.dump(configs, fw, indent=2)

    def save_model(self, output_path):
        '''
        Save model state to the file.

        Parameters:
            output_path : Path were the model weights will be saved.

        Return:
            None
        '''
        Path(output_path).parent.mkdir(exist_ok=True)

        torch.save(self.model.state_dict(), output_path)
        self._save_configs(Path(output_path))

    def load_model(self, model_path):
        '''
        Load model from the path

        Parameters:
            model_path : Path to the model weights should be loaded.

        Return:
            None
        '''
        self.model.load_state_dict(model_path)
