'''
Aerogel txt file IO
'''
from pathlib import Path

from .file_io import FileIO
from .reader_structs import (AERO_FILE_AEROGEL_LINES, AERO_FILE_TOPOLOGY_LINES, AERO_FILE_PARAMS)

class AerogelIO(FileIO):
    '''
    Aerogel file handler
    '''
    def __init__(self, name=None):
        '''
        Init method
        '''
        super().__init__(name)
        self.position = AERO_FILE_TOPOLOGY_LINES
        self.params = AERO_FILE_PARAMS
        self.lines = AERO_FILE_AEROGEL_LINES

    def read_file(self, input_path: Path) -> dict:
        '''
        Read from the txt file and convert it to dict

        Parameters:
            input_path: Path to the aerogel parameters file

        Return:
            file_data: Preprocessed data from text file
        '''
        file_raw_data = open(input_path).readlines()
        file_data = {}
        for line in file_raw_data:
            line_struc = self._clean_line(line)
            lid = int(line_struc[1])
            pid = int(line_struc[0])
            for j, value in enumerate(line_struc[2:]):
                file_data[f'{self.lines[lid]}_{self.position[pid]}_{self.params[j]}'] = float(value)
        return file_data

    def create_file(self, output_path: Path, temp_path: Path, evt_data: dict) -> None:
        raise NotImplementedError('Aerogel file creation method not implemented \
as it should be generated from simulations!')
