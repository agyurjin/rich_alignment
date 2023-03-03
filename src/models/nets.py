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
        modules = [nn.Linear(params['input_layer'], params['hidden_layer_neurons'][0])]
        for i in range(len(params['hidden_layer_neurons'])-1):
            modules.append(nn.Sigmoid())
            modules.append(nn.Linear(params['hidden_layer_neurons'][i], params['hidden_layer_neurons'][i+1]))
        last_hidden_id = len(params['hidden_layer_neurons']) - 1
        modules.append(nn.Sigmoid())
        modules.append(nn.Linear(params['hidden_layer_neurons'][last_hidden_id], params['output_layer']))

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
