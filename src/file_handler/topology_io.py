'''
Topology file IO
'''
#from __future__ import absolute_import
from pathlib import Path

from .file_io import FileIO
from .reader_structs import TOP_FILE_PARAMS

class TopologyIO(FileIO):
    '''
    Topology file class
    '''
    def __init__(self, name=None):
        '''
        Init method
        '''
        super().__init__(name)
        self.params = TOP_FILE_PARAMS

    def read_file(self, input_path: Path) -> dict:
        '''
        Read file and parse it to the dict

        Parameters:
            input_path: Path to the input file

        Return:
            file_data: Parsed dictinory
        '''
        file_raw_data = self.read_input_file(input_path)
        file_data = {}
        for line in file_raw_data:
            line_struc = self._clean_line(line)
            layer_id = int(line_struc[0]) + 1
            tile_id = int(line_struc[1]) + 1
            for j, value in enumerate(line_struc[2:]):
                key_name = f'{self.name}_aerogel_b{layer_id}_tile_{tile_id}_{self.params[j]}'
                file_data[key_name] = float(value)
        return file_data

    def create_file(self, output_path: Path, temp_path: Path, evt_data: dict) -> None:
        '''
        Read template file and create similar file with new parameters

        Parameters:
            output_path: Output file path
            temp_path: Template file path
            evt_data: Data to ochange in the new file

        Return:
            None
        '''
        raise NotImplementedError('Topology file creation method not implemented \
as it should be created during the simulation!')
