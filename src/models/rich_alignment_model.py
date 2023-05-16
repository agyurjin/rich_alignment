#from .base_model import BaseModel
#from nets import fcn
from .nn_model import NNModel

class RICHAlignmentModel():
    def __init__(self, model_data):
        self.model = None 
        if model_data['type'] == 'nn':
            self.model = NNModel(model_data)
        else:
            raise NotImplementedError

    def train(self, output_path, dataloader, iter_num, optimizer_data):
        self.model.train(dataloader, iter_num, optimizer_data)
        res = self.model.save_model(output_path)
        return res

    def predict(self, x):
        return self.model.predict(x)

    def load_model(self, model_path, norm_path):
        self.model.load_model(model_path, norm_path)

        


