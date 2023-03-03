'''
Predictor module
'''
from .gen_minimizer import GenMinimizer
from .sgd_minimizer import SGDMinimizer

class Minimizer:
    '''
    Minimizator class
    '''
    def __init__(self, model, configs):
        '''
        Init function

        Parameters:
            model (Predictor): Loaded model for predictions
            configs (dict): Loaded minima_configs.json file
        '''
        self.strategy = None

        self.args = {
            'iters': configs['MINIMA']['iters'],
            'number_of_samples': configs['MINIMA']['number_of_samples']
            }

        if configs['MINIMA']['type'] == 'sgd':
            self.args['momentum'] = configs['MINIMA']['momentum']
            self.strategy = SGDMinimizer(model)
        elif configs['MINIMA']['type'] == 'genetic':
            self.strategy = GenMinimizer(model)

    def find_minima(self, in_space):
        '''
        Find mimia in the input space

        Parameters:
            in_space (dict): Input spcae

        Return:
            min_point (): Calculated minima
            min_error (): Convergence error for minima
            pos_error (): Positive error from MINUIT
            neg_error (): Negative error from MINUIT
        '''

        self.strategy.set_precisions(in_space['precisions'])
        min_point, min_error = self.strategy.minimize(in_space, **self.args)
        pos_error = self.strategy.min_error_calc(min_point, sigma=None, up=1, iters=10000, step=0.1, limit=100)
        neg_error = self.strategy.min_error_calc(min_point, sigma=None, up=1, iters=10000, step=-0.1, limit=-100)
        self._do_prints(min_point, min_error, pos_error, neg_error)

        return min_point, min_error, pos_error, neg_error

    def _do_prints(self, min_point, min_error, pos_error, neg_error):
        '''
        Some printings

        Parameters:
            min_point (): Calculated minima
            min_error (): Convergence error for minima
            pos_error (): Positive error from MINUIT
            neg_error (): Negative error from MINUIT
        '''
        header = '*'*5 + ' RESULTS ' + '*'*5
        print(header)
        print('-'*len(header))
        print('CONVERGENCE ERROR')
        for i in range(len(min_point)):
            print(f'{min_point[i]} +/- {min_error[i]}')

        print('-'*len(header))
        print('MINUIT ERROR')
        for i in range(len(min_point)):
            print(f'{min_point[i]} + {pos_error[i]} - {neg_error[i]}')
        print('-'*len(header))
