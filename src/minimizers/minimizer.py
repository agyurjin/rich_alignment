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
        pos_error = self.strategy.min_error_calc(min_point, None, 1, 10000, 0.1, 100)
        neg_error = self.strategy.min_error_calc(min_point, None, 1, 10000, -0.1, -100)
        self._do_prints(min_point, min_error, pos_error, neg_error)

        return min_point, min_error, pos_error, neg_error

    @staticmethod
    def _do_prints(min_point, min_error, pos_error, neg_error):
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
        print('STATISTICAL ERROR')
        for min_p, min_e in zip(min_point, min_error):
            print(f'{min_p:.5} +/- {min_e:.5}')

        print('-'*len(header))
        print('MINUIT ERROR')
        for min_p, pos_e, neg_e in zip(min_point, pos_error, neg_error):
            print(f'{min_p:.5} + {pos_e:.5} - {neg_e:.5}')
        print('-'*len(header))
