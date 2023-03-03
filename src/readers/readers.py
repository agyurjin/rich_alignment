'''
Possible readers
'''
from .base_reader_strategy import BaseReader

class GeometryReader(BaseReader):
    '''
    Geometry reader
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
        self.geo_params = ['x', 'y', 'z']
        self.angle_params = ['theta_x', 'theta_y', 'theta_z'] 

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
            lid = i // 3
            line_split = line.split(' ')
            if i % 3 == 0:
                continue

            params = self.geo_params if i % 3 == 1 else self.angle_params

            for j, param in enumerate(params):
                file_data['{}_{}'.format(self.layers[lid], param)] = float(line_split[j])

        return file_data

class AerogelReader(BaseReader):
    '''
    Aerogel data reader
    '''
    def __init__(self):

        self.position = ['dp', 'a2l', 'a2r', 'a3', 's5c_b1', 's5c_b2', 'other']
        self.params = ['mean', 'mean_err', 'std', 'std_err', 'entries', 'chi2']
        self.layers = ['aerogel_b1', 'aerogel_b2', 'aerogel_b3']

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
            lid = i // 3
            line_split = line.split(' ')
            line_split_clean = [v for v in line_split if v != '']
            for j, param in enumerate(self.params):
                file_data['{}_{}_{}'.format(self.layers[i%3], self.position[lid], param)] \
                    = float(line_split_clean[j+2])

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
                


