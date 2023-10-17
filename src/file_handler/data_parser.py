'''
Main file to read and write data files
'''
from pathlib import Path

from .geometry_io import GeometryIO
from .optical_io import OpticalIO
from .aerogel_io import AerogelIO
from .topology_io import TopologyIO
from .mapmt_io import MapmtIO
from .variance_io import VarianceIO
from .tracks_io import TracksIO

from .reader_structs import TOP_FILE_NAMES

class DataParser:
    '''
    Data parser
    '''
    def __init__(self):
        '''
        init method
        '''
        self.strategy = None

    def _set_strategy(self, file_path: Path) -> None:
        '''
        Set strategy for file reading from file name

        Parameters:
            file_path: Path to the input file

        Return:
            None
        '''
        file_name = file_path.name
        file_suffix = file_path.suffix
        if 'Geometry' in file_name and file_suffix == '.dat':
            self.strategy = GeometryIO()
        elif 'Variance' in  file_name and file_suffix == '.dat':
            self.strategy = VarianceIO()
        elif 'Optical' in file_name and file_suffix == '.dat':
            self.strategy = OpticalIO()
        elif 'Aerogel' in file_name and file_suffix == '.out':
            self.strategy = AerogelIO()
        elif 'MAPMT' in file_name and file_suffix == '.out':
            self.strategy = MapmtIO()
        elif 'Tracks' in file_name and file_suffix == '.out':
            self.strategy = TracksIO()
        elif file_suffix == '.out':
            for name in TOP_FILE_NAMES:
                if name in file_name:
                    self.strategy = TopologyIO(name)
                    break
        else:
            err_str = '"'+'","'.join(TOP_FILE_NAMES)+'"'
            raise TypeError(f'File cannot be handeled!!! Check for possible solutions.\n \
1. Geometry data file name should contain "Geometry" word and have ".dat" extension\n \
2. Optical data file name should contain "Optical" word and have ".dat" extension\n \
3. Aerogel output file name should contain "Aerogel" word and have ".out" extension\n \
4. Any topology file name should contain {err_str} word and have ".out" extension')

    def read_file(self, file_path: Path) -> dict:
        '''
        Use the file name to define strategy and convert file to the dictinory

        Parameters:
            file_path: Path to the input file

        Return:
            data_dict: Converted data dictinory
        '''
        self._set_strategy(file_path)
        data_dict = self.strategy.read_file(file_path)
        return data_dict

    def create_file(self, output_path: Path, temp_path: Path, evt_dict: dict) -> None:
        '''
        Read template file and create similar file with new parameters
        with the defined strategy

        Parameters:
            output_path: Output file path
            temp_path: Template file path
            evt_dict: Data to change in the new file

        Return:
            None
        '''
        self._set_strategy(temp_path)
        self.strategy.create_file(output_path, temp_path, evt_dict)
