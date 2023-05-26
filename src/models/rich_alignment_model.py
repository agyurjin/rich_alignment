'''
RICH Alignment Model
'''
from .nn_model import NNModel

class RICHAlignmentModel():
    '''
    Create model from provied data
    '''
    def __init__(self, model_data):
        '''
        Init method

        Parameters:
            model_data: Model meta data
        '''
        self.model = None
        if model_data['type'] == 'nn':
            self.model = NNModel(model_data)
        else:
            raise NotImplementedError

    def train(self, output_path, datareader, train_info):
        '''
        Train model

        Parameters:
            output_path:
            datareader:
            train_info

        Return:
            res
        '''
        self.model.train(datareader, train_info)
        res = self.model.save_model(output_path)
        return res

    def predict(self, x):
        '''
        Predict for provided points

        Parameters:
            x: Provided points

        Return:
            y_pred: Predicted values
        '''
        y_pred = self.model.predict(x)
        return y_pred

    def load_model(self, model_path, norm_path):
        '''
        Load model and normalization parameters

        Parameters:
            model_path: Model state dict path
            norm_path: Normalization JSON path
        '''
        self.model.load_model(model_path, norm_path)
