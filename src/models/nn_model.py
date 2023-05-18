'''
NN model
'''
import sys
import json
from pathlib import Path
from copy import deepcopy
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
        self.model = fcn(configs)
        self.loss_hist = {'train_loss': [], 'val_loss':[], 'epochs':[]}
        self.norm_params = {'x_mean': [], 'x_std': [], 'y_mean': [], 'y_std': []}

    def train(self, data_loader, epochs, optimizer_data):
        lr = optimizer_data['lr'] if 'lr' in optimizer_data else 1e-2
        momentum = optimizer_data['momentum'] if 'momentum' in optimizer_data else 0.9

        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=lr, momentum=momentum)

        running_loss = 0
        best_model = None
        best_loss = 1e10
        verbose = 1000
        prev_val_loss = 1e10

        x_train, y_train = data_loader.get_trainset()
        x_val, y_val = data_loader.get_testset()
        
        x_train_mean = x_train.mean(axis=0)
        y_train_mean = y_train.mean(axis=0)
        x_train_std = x_train.std(axis=0)
        y_train_std = y_train.std(axis=0)

        self.norm_params['x_mean'] = x_train_mean
        self.norm_params['x_std'] = x_train_std
        self.norm_params['y_mean'] = y_train_mean
        self.norm_params['y_std'] = y_train_std

        x_train = (x_train - x_train_mean)/(x_train_std+1e-5)
        y_train = (y_train - y_train_mean)/(y_train_std+1e-5) 
        x_val = (x_val - x_train_mean)/(x_train_std+1e-5)
        y_val = (y_val - y_train_mean)/(y_train_std+1e-5)
        
        for i in range(epochs):
            optimizer.zero_grad()
            y_pred = self.model(x_train)
            loss_v = loss_fn(y_pred, y_train)
            loss_v.backward()
            optimizer.step()
            running_loss += float(loss_v)
        
            if (i+1) % verbose == 0: 
                with torch.no_grad():
                    y_pred = self.model(x_val)
                    loss_v = loss_fn(y_pred, y_val)
                    val_loss = float(loss_v)
                if val_loss < best_loss:
                    best_model = deepcopy(self.model)
                    best_loss = val_loss

                print('*'*20)
                print(f'[TRAINING] Epoch {i+1}/{epochs}')
                print(f'[TRAINING] train loss: {running_loss/verbose:.5f}')
                print(f'[TRAINING] val loss: {val_loss:.5f}')
                print('*'*20)
                self.loss_hist['train_loss'].append(running_loss/verbose)
                self.loss_hist['val_loss'].append(val_loss)
                self.loss_hist['epochs'].append(i+1)
                running_loss = 0


        if best_model is not None:
            self.model = best_model

    def predict(self, x):
        x = (x - self.norm_params['x_mean'])/self.norm_params['x_std']
        with torch.no_grad():
            y_pred = self.model(x)
        y_pred = y_pred * self.norm_params['y_std'] + self.norm_params['y_mean']
        return y_pred

    def save_model(self, output_path):
        '''
        Save model state to the file.

        Parameters:
            output_path : Path were the model weights will be saved.

        Return:
            None
        '''
        model_name = 'model.pth'
        model_config_name = 'model_config.json'
        loss_hist_name = 'loss_hist.json'

        res = {}
        res['x_mean'] = self.norm_params['x_mean'].tolist()
        res['x_std'] = self.norm_params['x_std'].tolist()
        res['y_mean'] = self.norm_params['y_mean'].tolist()
        res['y_std'] = self.norm_params['y_std'].tolist()      

        torch.save(self.model.state_dict(), output_path/model_name)
        with open(output_path/loss_hist_name, 'w') as fw:
            json.dump(self.loss_hist, fw)

        with open(output_path/model_config_name, 'w') as fw:
            json.dump(res, fw)

        res = {
            'model_name': model_name,
            'model_config_name': model_config_name,
            'loss_hist_name': loss_hist_name 
        }
        return res

    def load_model(self, model_path, norm_path):
        '''
        Load model from the path

        Parameters:
            model_path : Path to the model weights should be loaded.

        Return:
            None
        '''
        self.model.load_state_dict(torch.load(model_path))
        norm_data = json.load(open(norm_path))
        x_mean = torch.tensor(norm_data['x_mean'])
        x_std = torch.tensor(norm_data['x_std'])
        y_mean = torch.tensor(norm_data['y_mean'])
        y_std = torch.tensor(norm_data['y_std'])
        self.norm_params = {'x_mean': x_mean, 'x_std': x_std, 'y_mean': y_mean, 'y_std': y_std}
