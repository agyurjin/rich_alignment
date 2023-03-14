'''
Possible readers
'''
from .base_reader_strategy import BaseReader
from .layers import (GEOMETRY_LAYERS, GEO_PARAMS, ANGLE_PARAMS, PHOTONS, PHOTON_PARAMS, PHOTON_LAYERS)

class GeometryReader(BaseReader):
    '''
    Geometry reader
    '''
    def __init__(self):
        self.layers = GEOMETRY_LAYERS
        self.geo_params = GEO_PARAMS
        self.angle_params = ANGLE_PARAMS 

    def __call__(self, file_path):
        '''
        Read data from the simulation output file

        Parameterss :
            file_path (Pathlike): Path to the geometry parameters file

        Return:
            file_data (dict): Preprocessed data from text file
        '''

        file_raw_data = open(str(file_path)).readlines()
        file_data = {}

        for i, line in enumerate(file_raw_data):
            if i % 3 == 0:
                continue
            lid = i // 3
            line_split = line.split(' ')
            line_split_clean = [v for v in line_split if v != '']
            params = self.geo_params if i % 3 == 1 else self.angle_params

            for j, value in enumerate(line_split_clean[:3]):
                file_data['{}_{}'.format(self.layers[lid], params[j])] = float(value)

        return file_data

class AerogelReader(BaseReader):
    '''
    Aerogel data reader
    '''
    def __init__(self):

        self.position = PHOTONS
        self.params = PHOTON_PARAMS
        self.layers = PHOTON_LAYERS

    def __call__(self, file_path):
        '''
        Parameterss:
            file_path (Pathlike): Path to the geometry parameters file

        Return:
            file_data (dict): Preprocessed data for text file
        '''

        file_raw_data = open(str(file_path)).readlines()

        file_data = {}
        for i, line in enumerate(file_raw_data):
            line_split = line.split(' ')
            line_split_clean = [v for v in line_split if v != '']
            lid = int(line_split_clean[1])
            pid = int(line_split_clean[0])
            for j, value in enumerate(line_split_clean[2:]):
                file_data['{}_{}_{}'.format(self.layers[lid], self.position[pid], self.params[j])] = float(value)

        return file_data


class OpticalReader(BaseReader):
    '''
    Optical parameters reader
    '''
    def __init__(self):
        self.layers = [
            'aerogel_b1',
            'aerogel_b2',
            'aerogel_b3',
            'frontal_mirror_b1',
            'frontal_mirror_b2',
            'planar_mirror_l',
            'planar_mirror_r',
            'bottom_mirror',
            'spherical_mirror',
            'mapmt'
        ]

        self.values = ['ref_index', 'Npe', 'smearing', 'efficiency']


    def __call__(self, file_path):

        file_raw_data = open(str(file_path)).readlines()

        file_data = {}
        for i, line in enumerate(file_raw_data):
            if i % 2 == 0:
                continue
            line_split = line.split(' ')
            line_split_clean  = [v for v in line_split if v != '']
            if len(line_split) > 2:
                for j, param in enumerate(line_split_clean):
                    if j == 1:
                        continue
                    file_data['{}_{}'.format(self.layers[i//2], self.values[j])] = float(param)
            else:
                for j, param in enumerate(line_split_clean):
                    file_data['{}_{}'.format(self.layers[i//2], self.values[j+2])] = float(param)

        return file_data 


class TileReader(BaseReader):
    def __init__(self):
        self.params = ['mean', 'mean_err', 'std', 'std_err', 'chi2']

    def __call__(self, file_path):
        file_raw_data = open(str(file_path)).readlines()

        file_data = {}
        for i, line in enumerate(file_raw_data):
            line_split = line.split(' ')
            line_split_clean = [v for v in line_split if v != '']
            layer_id = int(line_split_clean[0]) + 1
            tile_id = int(line_split_clean[1]) + 1
            for j, value in enumerate(line_split_clean[2:]):
                file_data['aerogel_b{}_tile_{}_{}'.format(layer_id, tile_id, self.params[j])] = float(value)

        return file_data
                


