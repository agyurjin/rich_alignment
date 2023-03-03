'''
Predictor module
'''
import torch
import numpy as np

class BaseMinimizer:
    def __init__(self, model):
        self.model = model

    def minimizer(self, in_space, **kwargs):
        pass

    def set_precisions(self, precisions):
        self.precisions = precisions

    def get_start_points(self, in_space, nums):
        points = []
        for i in range(nums):
            point = []
            for val_min, val_max, _  in in_space['space']:
                point.append((val_max - val_min)*np.random.random() + val_min)
            points.append(point)
        return np.array(points)

    def min_error_calc(self, point, sigma, up, iters, step, limit):
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
