'''
Useful functions
'''
import numpy as np
import torch

def create_grid(keywords):
    '''
    Create grid for prediction

    Parameters:
        keywords (dict): Keywords dictinory from JSON file

    Return:
        points (np.array): Points that should be used for plotting the model
        kw_names (list): All input keywords names that exists is True
    '''
    grids = []
    kw_names = []
    keywords = keywords['INPUT']['GEOMETRY'] + keywords['INPUT']['OPTICAL']
    for keyword in keywords:
        for key, value in keyword.items():
            if value['exists']:
                grids.append(np.linspace(*value['grid']))
                kw_names.append(key)

    if len(grids) == 1:
        points = grids[0].reshape((len(grids[0], 1)))
    else:
        v1, v2 = np.meshgrid(grids[0], grids[1])
        v1 = v1.flatten()
        v1 = v1.reshape((len(v1), 1))
        v2 = v2.flatten()
        v2 = v2.reshape((len(v2), 1))
        points = np.hstack((v1, v2))

    return points, kw_names

def do_prediction(model, points):
    '''
    Do predictions

    Parameters:
        model (): Provided model
        points (torch.tensor): Points for predictions with provided model

    Return:
        chi2 (np.array): Predictions for each point
    '''
    chi2 = []
    for point in points:
        point = torch.tensor(point, dtype=torch.float)
        chi2.append(model.predict(point).detach().numpy())

    return np.array(chi2)

def create_workspace(keywords, precisions):
    '''
    Use keyword.json and precisions to generate input space and output space

    Parameters:
        keywords (dict): Loaded keyword.json file
        precisions (dict): Precisions for each feature

    Return:
        in_space (dict): Input features information
        out_space (dict): Output features information
    '''
    in_space = {'space': [], 'names': [], 'precisions': []}
    out_space = {'names': []}

    input_keywords = keywords['INPUT']['GEOMETRY'] + keywords['INPUT']['OPTICAL']
    for inkw in input_keywords:
        for name, value in inkw.items():
            if value['exists']:
                in_space['space'].append(value['grid'])
                in_space['names'].append(name)
                feature_is = 'distance'
                if name.find('theta') > 0:
                    feature_is = 'angle'
                elif name.find('ref_index') > 0:
                    feature_is = 'ref_index'
                in_space['precisions'].append(precisions[feature_is])

    output_keywords = keywords['OUTPUT']['AEROGEL']
    for outkw in output_keywords:
        for name, value in outkw.items():
            if value['exists']:
                out_space['names'].append(name)

    return in_space, out_space

def get_keyword_names(keywords):
    '''
    Parameters:
        keywords (dict): Loaded keyword.json file

    Return:
        in_kw_names (list): Input keywords names
        out_kw_names (list): Output keywords names
    '''
    in_kw_names = []
    out_kw_names = []

    for keyword in keywords['INPUT']['GEOMETRY'] + keywords['INPUT']['OPTICAL']:
        for key, value in keyword.items():
            if value['exists']:
                in_kw_names.append(key)

    for keyword in keywords['OUTPUT']['AEROGEL']:
        for kw, value in keyword.items():
            if value['exists']:
                out_kw_names.append(kw)
    return in_kw_names, out_kw_names
