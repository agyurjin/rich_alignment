'''
Abstract model class
'''
from abc import ABC, abstractmethod

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
    def train(self, data_reader, train_info):
        '''
        Train model and keep best on validation set

        Parameters:
            data_reader: DataReader object to get data
            train_info: Trinaing metadatas

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
    def load_model(self, model_path, norm_path):
        '''
        Load already saved model

        Parameters:
            model_path (Path or str): Path to the model weights.
                Config file should be in the same level.
            norm_path: Mean and STD values from trained model
        '''
