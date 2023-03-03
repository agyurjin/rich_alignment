'''
'''
import torch
import numpy as np
from tqdm import tqdm
from .base_minimizer import BaseMinimizer

class GenMinimizer(BaseMinimizer):
    '''
    '''
    def __init__(self, model):
        super().__init__(model)

    def minimize(self, in_space, **kwargs):
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

        return new_points[0], np.zeros_like(new_points[0])

    def _generat_points(self, points, **kwargs):
        # crossover step
        crosses = []
        while len(crosses) < kwargs['number_of_samples']:
            rands = points[np.random.randint(0,len(points),2)]
            crosses.append(rands.mean(axis=1))
            crosses.append(np.append(rands[0, :len(rands[0])//2], rands[1, len(rands[1])//2:]))
            crosses.append(np.append(rands[1, :len(rands[1])//2], rands[0, len(rands[0])//2:]))

        # mutation step
        def mut_coef():
            yield 2*(np.random.rand()-0.5)

        for cross in crosses:
            idx = np.random.randint(len(cross))
            cross[idx] +=  (5*next(mut_coef())*self.precisions[idx])

        return np.array(crosses)

    def _get_fitness(self, points):
        fitness = []
        with torch.no_grad():
            for point in points:
                x = torch.tensor(point, dtype=torch.float)
                fitness.append(float(self.model.predict(x).mean()))
        return fitness    
