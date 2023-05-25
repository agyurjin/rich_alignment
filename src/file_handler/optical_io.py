'''
Optical file IO
'''
#from __future__ import absolute_import
from pathlib import Path

from .file_io import FileIO
from .reader_structs import (OPT_FILE_LINES, OPT_FILE_PARAMS)

class OpticalIO(FileIO):
    '''
    Optical file class
    '''
    def __init__(self, name=None):
        '''
        Init method
        '''
        super().__init__(name)
        self.lines = OPT_FILE_LINES
        self.params = OPT_FILE_PARAMS

    def read_file(self, input_path: Path) -> dict:
        '''
        Read data from the optical file

        Parameters:
            input_path: Path to the optical file parameters

        Return:
            file_data: Preprocessed data
        '''
        file_raw_data = self.read_input_file(input_path)
        file_data = {}
        for i, line in enumerate(file_raw_data):
            if i % 2 == 0:
                continue
            line_struc = self._clean_line(line)
            line_name = self.lines[i//2]
            idx = None
            shift = None
            if 'aerogel' in line_name:
                idx, shift = [0,1,2,3], 0
            elif 'mapmt' in line_name:
                idx, shift = [3,4], 3
            else:
                idx, shift = [2,3], 2
            for j in idx:
                file_data[f'{line_name}_{self.params[j]}'] = float(line_struc[j-shift])
        return file_data

    def create_file(self, output_path: Path, temp_path: Path, evt_data) -> None:
        '''
        Read optical file template and create similar optical file with new parameters

        Parameters:
            output_path: Output file path
            temp_path: Template file path
            evt_data: Data to change in generated optical file
        '''
        temp_data = self.read_input_file(temp_path)
        self.lines = {v:k for k,v in self.lines.items()}
        self.params = {v:k for k,v in self.params.items()}
        for key, value in evt_data.items():
            line_num, param_num = self._kw_to_pos(key)
            line = temp_data[line_num]
            line = self._clean_line(line)
            line[param_num] = f'{value:.6}'
            temp_data[line_num] = ' '.join(line) + '\n'

        with open(output_path, 'w', encoding="utf8") as file_writer:
            file_writer.write(''.join(temp_data))

    def _kw_to_pos(self, keyword: str) -> tuple:
        '''
        Use keywrod to find line and position for change

        Parameters:
            keyword: Parameter to change in optical file

        Return:
            line_num: Line number in the file
            param_num: Position nubmer in the line
        '''
        line_num = 1
        for key in self.lines.keys():
            if f'{key}_' in keyword:
                line_num += (self.lines[key]*2)
                break
        param_num = None
        for param in self.params:
            if f'_{param}' in keyword:
                param_num = self.params[param]
        if 'aerogel_' in keyword:
            shift = 0
        elif 'mapmt_' in keyword:
            shift = 3
        else:
            shift = 2
        param_num -= shift

        return line_num, param_num
