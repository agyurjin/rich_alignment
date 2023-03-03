'''
SGD minimizer module
'''
import torch
import numpy as np
from tqdm import tqdm
from .base_minimizer import BaseMinimizer

class SGDMinimizer(BaseMinimizer):
    '''
    SGD minimizer algorithm
    '''
    def __init__(self, model):
        '''
        Init function

        Parameters:
            model (Predictor): Loaded model for prediction
        '''
        super().__init__(model)

    def minimize(self, in_space, **kwargs):
        '''
        Minima finding algorithm

        Parameters:
            in_space (dict): Input space information
            **kwargs (dict): Useful information

        Return:
            min_point (torch.tensor): Calculated minima
            min_error (np.array): Calculated error from convergence
        '''
        start_points = self.get_start_points(in_space, kwargs['number_of_samples'])

        positions = None
        mins = []
        for point in tqdm(start_points):
            min_point, position = self.sgd_momentum(point, **kwargs)
            mins.append(min_point.numpy())
        mins = np.array(mins)
        mins = mins[np.any(~np.isnan(mins), axis=1), :]

        min_point = mins.mean(axis = 0)
        min_error = mins.std(axis = 0)
        return min_point, min_error

    def sgd_momentum(self, start_pos, **kwargs):
        '''
        Minimiz with stochastic gradient descent with momentum

        Parameters:
            start_pos (list): Minimization starting point

        Return:
            x (torch.tensor): Minimial point
            positions (list): List of point sgd moved during minimization
        '''
        grad_args = {}
        x = torch.tensor(start_pos, dtype=torch.float)
        v = torch.zeros_like(x)
        positions = [x]
        lr = 0.1*torch.tensor(self.precisions, dtype=torch.float)
        steps = torch.tensor(self.precisions, dtype=torch.float)

        with torch.no_grad():
            for _ in range(kwargs['iters']):
                grad_args = {'step': steps}
                grad = self._grad_calc(x, **grad_args)
                if (grad**2).sum() < 1e-5:
                    break

                v = kwargs['momentum'] * v + (1 - kwargs['momentum'])*grad
                x = x - lr * v
                positions.append(x)
        return x, positions

    def _grad_calc(self, point, **kwargs):
        '''
        Gradient calculation method at point

        Parameters:
            point (np.array): Gradient calculation point
            **kwargs (dict): Useful information

        Return:
            grad (list): Gradient at provieded point
        '''
        grad = torch.zeros_like(point)
        for i in range(point.size()[0]):
            point_step = point.clone()
            point_step[i] += kwargs['step'][i]
            y_init = self.model.predict(point).sum()
            y_step = self.model.predict(point_step).sum()
            grad[i] = (y_step - y_init) / kwargs['step'][i]
        return grad
