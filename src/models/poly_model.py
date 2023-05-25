'''
Polygon model
'''
import numpy as np
import torch
import json

from .base_model import BaseModel
from sklearn.linear_model import LinearRegression

#TODO: DOESN'T MATCH TO BASE CLASS
class PolyModel(BaseModel):
    '''
    Polygon model
    '''
    def __init__(self, configs):
        '''
        Initialize model
        '''
        super().__init__()
        self.norm = configs['norm']
        self.model = LinearRegression()


    def train(self, x_train, y_train, x_val, y_val):
        '''
        Train model and keep best on validation set

        Parameters:
            x_train: (N', F) dimensional tensor for training features
            y_train: (N', T) dimensional tensor for training targets
            x_val: (N", F) dimensional tensor for validation features
            y_val: (N", T) dimensional tensor for validation targets

        Return:
            None
        '''
        x_train = np.hstack((torch.ones(x_train.size[0],1), x_train, x_train**2))
        x_val = np.hstack((torch.ones(x_val.size[0],1), x_val, x_val**2))

        if self.norm:
            x_train, y_train = self._preprocess_data(x_train, y_train)
            x_val, y_val = self._preprocess_data(x_val, y_val)

        self.model.fit(x_train, y_train)

        y_val_pred = self.model.predict(x_val)
        mse_loss = torch.mean((y_val_pred - y_val)**2)
        print('val loss: {}'.format(mse_loss))

    def save_model(self, output_path):
        '''
        Save model coefficients to the file


        Paramters:
            output_path (str or Path): Path were the model configs will be saved

        Return:
            None
        '''
        configs = {
            'norm': {
                'x_means': self.data_means[:self.feature_size].tolist(),
                'x_std': self.data_stds[:self.feature_size].tolist(),
                'y_means': self.data_means[self.feature_size:].tolist(),
                'y_stds': self.data_std[self.feature_size:].tolist()
            
            },
            'weights': self.model.coef_.tolist()
        }
        
        with open(str(output_path), 'w') as fw:
            json.dump(configs, fw, indent=2)


    def load_model(self):
        pass
