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
        mins = []
        errors = []
        prev_best_points = None
        for i in tqdm(range(kwargs['iters'])):
            points = self.get_start_points(in_space, kwargs['number_of_samples'])
            for _ in range(100):
                fitness = self._get_fitness(points)

                best_points = points[np.argsort(fitness)][:int(0.2*len(points))+1]
                
                if prev_best_points is not None:
                    if ((prev_best_points - best_points)**2).mean() < 1e-4:
                        break
                prev_best_points = best_points
                crosses = self._generat_points(best_points, in_space, **kwargs)
                cross_fitness = self._get_fitness(crosses)
                all_fitnesses = fitness + cross_fitness
                points = np.vstack((points, crosses))
                new_points = points[np.argsort(all_fitnesses)][:kwargs['number_of_samples']]
                points = new_points
            mins.append(new_points[0])
        
        mins = np.array(mins)
        min_point = mins.mean(axis=0)
        min_error = mins.std(axis=0)
        
        return min_point, min_error

    def _generat_points(self, points, in_space, **kwargs):
        '''
        Generate new points

        Parameters:
            points (np.array): Generated points
            in_space : heto
            **kwargs (dict): Useful information

        Return:
            crosses (np.array): Crossed and mutated points
        '''
        crosses = []
        while len(crosses) < kwargs['number_of_samples']:
            rands = points[np.random.randint(0,len(points),len(points)//2)]
            crosses.append(rands.mean(axis=0))
            crosses.append(np.append(rands[0, :len(rands[0])//2], rands[1, len(rands[1])//2:]))
            crosses.append(np.append(rands[1, :len(rands[1])//2], rands[0, len(rands[0])//2:]))

        def mut_coef():
            yield 2*(np.random.rand()-0.5)

        for cross in crosses:
            idx = np.random.randint(len(cross))
            temp_v = (5*next(mut_coef())*self.precisions[idx])
            if temp_v > 0:
                cross[idx] = min(cross[idx]+temp_v, in_space['space'][idx][1])
            else:
                cross[idx] = max(cross[idx]+temp_v, in_space['space'][idx][0])
        return np.array(crosses)

    def _get_fitness(self, points):
        '''
        Get fitness value for points

        Parameters:
            points (np.array): Selected points

        Return:
            fitness (list): Fitness of each point
        '''
        points = torch.tensor(points, dtype=torch.float)
        fitness = self.model.predict(points).sum(axis=1).tolist()
        return fitness
