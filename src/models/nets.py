'''
Simple net for testing
'''
from torch import nn

class fcn(nn.Module):
    '''
    Fully connected network
    '''
    def __init__(self, params):
        '''
        Craete fcn with parameters

        Parameters:
            params (dict): Parameters to create network
        '''
        super(fcn, self).__init__()
        layers = [params['input_layer']] + params['hidden_layer_neurons']
        modules = []
        for i in range(len(layers)-1):
            modules.append(nn.Linear(layers[i], layers[i+1]))
            modules.append(nn.Sigmoid())
#            modules.append(nn.BatchNorm1d(layers[i+1]))
        modules.append(nn.Linear(layers[len(layers) - 1], params['output_layer']))

        self.net = nn.Sequential(*modules)


    def forward(self,x):
        '''
        Forward pass

        Parameters:
            x (torch.tensor): () dims input tensor

        Return:
            y_pred (torch_tensor): () dims output tensor
        '''
        y_pred = self.net(x)
        return y_pred
