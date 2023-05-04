'''
Geometry file IO
'''
#from __future__ import absolute_import

from .file_io import FileIO
from .reader_structs import (GEO_FILE_LINES_V1, GEO_FILE_LINES_V2,
 GEO_FILE_EUCLIDE_PARAMS, GEO_FILE_ANGLE_PARAMS)

class GeometryIO(FileIO):
    '''
    Geomtery file class
    '''
    def __init__(self):
        '''
        Init method
        '''
        super().__init__()
        self.geo_params = GEO_FILE_EUCLIDE_PARAMS
        self.angle_params = GEO_FILE_ANGLE_PARAMS

    def read_file(self, input_path: str) -> dict:
        '''
        Read data from the simulation output file

        Parameterss:
            file_path: Path to the geometry parameters file

        Return:
            file_data: Preprocessed data from text file
        '''
        file_raw_data = open(input_path).readlines()
        self.lines = GEO_FILE_LINES_V1 if len(file_raw_data) == 30 else GEO_FILE_LINES_V2
        file_data = {}
        for i, line in enumerate(file_raw_data):
            if i % 3 == 0:
                continue
            lid = i // 3
            line_struc = self._clean_line(line)
            params = self.geo_params if i % 3 == 1 else self.angle_params
            for j, value in enumerate(line_struc[:3]):
                file_data[f'{self.lines[lid]}_{params[j]}'] = float(value)
        return file_data

    def create_file(self, output_path: str, temp_path: str, evt_data: dict) -> None:
        '''
        Read geometry template file eand create similar geometry file with new parameters

        Parameters:
            output_path: Output file path
            temp_path: Template file path
            evt_data: Data to change in generated geometry file

        Return:
            None
        '''
        temp_data = open(temp_path).readlines()
        self.lines = GEO_FILE_LINES_V1 if len(temp_data) == 30 else GEO_FILE_LINES_V2
        self.lines = {v:k for k,v in self.lines.items()}
        self.geo_params = {v:k for k,v in self.geo_params.items()}
        for key,value in evt_data.items():
            line_num, param_num = self._kw_to_pos(key)
            line = temp_data[line_num]
            line = self._clean_line(line)
            value = f'{value:.3}' if  line_num%3==2 else f'{value:.4}'
            line[param_num] = value
            temp_data[line_num] = ' '.join(line) + '\n'
        with open(output_path, 'w') as file_writer:
            file_writer.write(''.join(temp_data))

    def _kw_to_pos(self, keyword: str) -> tuple:
        '''
        Use keyword to find the line and position for change

        Parameters:
            keyword: Parameter to change in the geometry file

        Return:
            line_num: Line number in the file
            param_num: Position number in the line
        '''
        line_num = 0
        for key in self.lines.keys():
            if f'{key}_' in keyword:
                line_num += (self.lines[key]*3)
                break
        shift = 2 if '_theta_' in keyword else 1
        line_num += shift
        param_num = None
        for geo_param in self.geo_params.keys():
            if f'_{geo_param}' in keyword:
                param_num = self.geo_params[geo_param]
                break
        return line_num, param_num
