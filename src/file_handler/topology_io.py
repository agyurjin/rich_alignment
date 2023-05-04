'''
Topology file IO
'''
#from __future__ import absolute_import

from .file_io import FileIO
from .reader_structs import TOP_FILE_PARAMS

class TopologyIO(FileIO):
    '''
    Topology file class
    '''
    def __init__(self):
        '''
        Init method
        '''
        super().__init__()
        self.params = TOP_FILE_PARAMS

    def read_file(self, input_path: str) -> dict:
        '''
        Read file and parse it to the dict

        Parameters:
            input_path: Path to the input file

        Return:
            file_data: Parsed dictinory
        '''
        file_raw_data = open(input_path).readlines()
        file_data = {}
        for line in file_raw_data:
            line_struc = self._clean_line(line)
            layer_id = int(line_struc[0]) + 1
            tile_id = int(line_struc[1]) + 1
            for j, value in enumerate(line_struc[2:]):
                file_data[f'aerogel_b{layer_id}_tile_{tile_id}_{self.params[j]}'] = float(value)
        return file_data

    def create_file(self, output_path: str, temp_path:str, evt_data: dict) -> None:
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
