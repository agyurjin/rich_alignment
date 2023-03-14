'''
Genetic algorithm module
'''
import torch
import numpy as np
from tqdm import tqdm
from .base_minimizer import BaseMinimizer

class GenMinimizer(BaseMinimizer):
    '''
    Genetic Algorithm minimizer
    '''
    def __init__(self, model):
        '''
        Init function

        Parameters:
            model (Predictor): Loaded model for predictions
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
            min_error (np.array): Calculated error (zeros only cannot calculate convergence)
        '''
        points = self.get_start_points(in_space, kwargs['number_of_samples'])
        for _ in tqdm(range(kwargs['iters'])):
            fitness = self._get_fitness(points)

            best_points = points[np.argsort(fitness)][:int(0.2*len(points))+1]

            crosses = self._generat_points(best_points, **kwargs)
            cross_fitness = self._get_fitness(crosses)
            all_fitnesses = fitness + cross_fitness
            points = np.vstack((points, crosses))
            new_points = points[np.argsort(all_fitnesses)][:kwargs['number_of_samples']]
            if np.all(points == new_points):
                break
            points = new_points

        min_point = new_points[0]
        min_error = np.zeros_like(new_points[0])
        return min_point, min_error

    def _generat_points(self, points, **kwargs):
        '''
        Generate new points

        Parameters:
            points (np.array): Generated points
            **kwargs (dict): Useful information

        Return:
            crosses (np.array): Crossed and mutated points
        '''
        crosses = []
        while len(crosses) < kwargs['number_of_samples']:
            rands = points[np.random.randint(0,len(points),2)]
            crosses.append(rands.mean(axis=0))
            crosses.append(np.append(rands[0, :len(rands[0])//2], rands[1, len(rands[1])//2:]))
            crosses.append(np.append(rands[1, :len(rands[1])//2], rands[0, len(rands[0])//2:]))

        def mut_coef():
            yield 2*(np.random.rand()-0.5)

        for cross in crosses:
            idx = np.random.randint(len(cross))
            cross[idx] +=  (5*next(mut_coef())*self.precisions[idx])

        return np.array(crosses)

    def _get_fitness(self, points):
        '''
        Get fitness value for points

        Parameters:
            points (np.array): Selected points

        Return:
            fitness (list): Fitness of each point
        '''
        fitness = []
        with torch.no_grad():
            for point in points:
                x = torch.tensor(point, dtype=torch.float)
                fitness.append(float(self.model.predict(x).mean()))
        return fitness
