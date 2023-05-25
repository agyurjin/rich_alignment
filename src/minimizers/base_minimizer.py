'''
Predictor module
'''
import torch
import numpy as np

class BaseMinimizer:
    '''
    Base minimizer class
    '''
    def __init__(self, model):
        '''
        Init function

        Parameters:
            model (Predictor): Loaded model for prediction
        '''
        self.model = model
        self.precisions = None

    def minimizer(self, in_space, **kwargs):
        '''
        Minima finding algorithm

        Parameters:
            in_space (dict): Input space information
            **kwargs (dict): Useful information
        '''

    def set_precisions(self, precisions):
        '''
        Set precisions for each feature

        Parameters:
            precisions (torch.tensor): All features precisions
        '''
        self.precisions = precisions

    @staticmethod
    def get_start_points(in_space, nums):
        '''
        Generate initial points in the input space

        Parameters:
            in_space (dict): Input space information
            nums (int): Number of inital points

        Return:
            points (np.array): Initial points
        '''
        points = []
        for _ in range(nums):
            point = []
            for val_min, val_max, _  in in_space['space']:
                point.append((val_max - val_min)*np.random.random() + val_min)
            points.append(point)
        points = np.array(points)
        return points

    def min_error_calc(self, point, sigma, up, iters, step, limit):
        #TODO: IMPOVE THIS FUNCTION
        '''
        MINUIT error calculation algorithm

        Parameters:
            point (torch.tensor):
            sigma (UNKNOWN): TO BE IMPLEMENTED
            up (float): Error calculation value
            iters (int): Number of iterations for fine calculation
            step (float): Size to find error range
            limit (float): Max error size point relative

        Return:
            errs (list): Calculated errors for the features
        '''
        errs = []
        point = torch.tensor(point, dtype=torch.float)
        y0 = self.model.predict(point).sum()
        for i in range(len(point)):
            curr_p = point.clone()
            up_step = None
            down_step = None
            j=1
            while True:
                if ((1 + j*step) - limit)*step > 0:
                    break
                curr_p[i] = point[i] + torch.abs(point[i])*j*step
                curr_y = self.model.predict(curr_p).sum()
                if (curr_y - y0) > 1:
                    up_step = point[i] + torch.abs(point[i])*j*step
                    down_step = point[i] + torch.abs(point[i])*(j-1)*step
                    break
                j+=1
            if up_step is None:
                errs.append(abs(float((abs(limit)-1)*point[i])))
                continue

            for k in range(iters):
                curr_p = point.clone()
                curr_p[i] = (up_step + down_step)/2
                curr_y = self.model.predict(curr_p).sum()
                if torch.abs((curr_y -y0) - up) < 1e-3:
                    errs.append(float(torch.abs(curr_p[i]-point[i])))
                    break
                if curr_y - y0 > 1:
                    up_step = curr_p[i]
                else:
                    down_step = curr_p[i]
            if (k+1) == iters:
                errs.append(float(torch.abs(curr_p[i]-point[i])))
        return errs
