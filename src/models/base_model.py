'''
Abstract model class
'''
from abc import ABC, abstractmethod
import torch

class BaseModel(ABC):
    '''
    Base model all models should inherit from this class
    '''
    def __init__(self):
        '''
        Initialize object
        '''
        self.data_means = None
        self.data_stds = None
        self.feature_size = None

    @abstractmethod
    def train(self, data_loader, epochs, optimizer_data):
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

    @abstractmethod
    def save_model(self, output_path):
        '''
        Save model state dict

        Parameters:
            output_path (Path or str): Path to save model weights.
                    Config file will be saveed in the same level.

        Return:
            None
        '''

    @abstractmethod
    def load_model(self, model_path):
        '''
        Load already saved model

        Parameters:
            model_path (Path or str): Path to the model weights.
                Config file should be in the same level.
        '''

    def _preprocess_data(self, x_set, y_set, train_set=True):
        '''
        Preprocess data

        Parameters:
            data (torch.tensor): (N, F+T) dimensional tensor stacked together featres and targets

        Return:
            data (torch.tensor): (N, F+T) dimensional tensor normalized data
        '''
        data = torch.hstack((x_set,y_set))
        self.feature_size = x_set.size()[1]

        if train_set:
            self.data_means = torch.mean(data, axis = 0) if self.norm else torch.zeros(data.size()[1])
            self.data_stds = torch.std(data, axis = 0) if self.norm else torch.ones(data.size()[1])

        # TODO: MAYBE NOT BEST SOLUTION. TRY TO FIND BETTER ONE!
        self.data_stds[self.data_stds == 0] = 1

        data = (data - self.data_means) / self.data_stds
        return data[:, :x_set.size()[1]], data[:, x_set.size()[1]:]

    def _postproces_data(self, data):
        '''
        Postprocess data

        Parameters:
            data (torch.tensor): (N, F+T) dimensional tensor normalized data

        Return:
            data (torch.tensor): (N, F+T) dimensional tensor real values
        '''
        return data * self.data_stds + self.data_means
