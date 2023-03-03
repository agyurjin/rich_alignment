'''
Run model for predictions and draw plots
'''
import json
from pathlib import Path
import numpy as np

from predictor import Predictor
from minimizers.minimizer import Minimizer

from utils import do_prediction, create_grid, create_workspace

from plotters import create_plots


def main():
    '''
    Main function
    '''
    minima_config_path = 'minima_config.json'
    minima_configs = json.load(open(minima_config_path))

    output_dir = Path(minima_configs['PATHS']['model_path'])
    model_config_path = output_dir / 'model_configs.json'
    model_path = output_dir / 'model.pth'

    model = Predictor(str(model_config_path))
    model.load_model(model_path)

    keywords = json.load(open(minima_configs['PATHS']['keywords_path']))
    in_space, out_space = create_workspace(keywords, precisions = minima_configs['MINIMA']['precisions'])

    minimizer = Minimizer(model, minima_configs)
    min_point, min_error, pos_error, neg_error = minimizer.find_minima(in_space)
    if len(min_point) <= 2:
        points, _ = create_grid(keywords)
        kw_names = {'in_kw_names': in_space['names'], 'out_kw_names': out_space['names']}
        assert len(kw_names) == len(min_point)
        chi2 = do_prediction(model, points)
        create_plots(chi2, points, str(output_dir / 'pred.pdf'), kw_names, min_point, min_error, pos_error, neg_error)

    x1 = np.array(min_point) + np.array([pos_error[0],0])
    x2 = np.array(min_point) + np.array([0,pos_error[1]])
    points = [min_point, x1, x2]
    chi2 = do_prediction(model, points)


if __name__ == '__main__':
    main()
