'''
Predictor module
'''
import json
import torch
from models.nets import fcn

class Predictor:
    '''
    Predictoor class to load trained model, do predictions and find minima.
    '''
    def __init__(self, configs_path):
        '''
        Init method load configs and creates model

        Parameters:
            configs_path (str or Path): Path to tained model JSON config file

        Return:
            None
        '''

        configs = json.load(open(configs_path))
        self.model = fcn(configs['net_structure'])
        self.norm = 'norm' in configs
        if self.norm:
            self.mean_x = torch.tensor(configs['norm']['x_means'], dtype=torch.float)
            self.std_x = torch.tensor(configs['norm']['x_stds'], dtype=torch.float)
            self.mean_y = torch.tensor(configs['norm']['y_means'], dtype=torch.float)
            self.std_y = torch.tensor(configs['norm']['y_stds'], dtype=torch.float)

    def load_model(self, model_path):
        '''
        Load trained model weights from the path

        Parameters:
            model_path (str or Path): Path to the model weights

        Return:
            None
        '''
        self.model.load_state_dict(torch.load(model_path))

    def predict(self, x):
        '''
        Do predictions with the loaded model

        Parameters:
            x (torch.tensor): () dims input tensor

        Return:
            y_pred (torch.tensor): () dims model predictions
        '''
        if self.norm:
            x = (x - self.mean_x) / self.std_x

        y_pred = self.model(x)

        if self.norm:
            y_pred = y_pred * self.std_y + self.mean_y

        return y_pred
