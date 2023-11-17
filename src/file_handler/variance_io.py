from pathlib import Path

from .file_io import FileIO
from .reader_structs import (VARIANCE_FILE_LINES, VARIANCE_PARAMS)

class VarianceIO(FileIO):
    '''
    '''
    def __init__(self, name=None):
        super().__init__(name)
        self.params = VARIANCE_PARAMS
        self.lines = VARIANCE_FILE_LINES
    

    def read_file(self, input_path: Path) -> dict:
        '''
        '''
        file_raw_data = self.read_input_file(input_path)
        file_data = {}
        lid = None
        for i, line in enumerate(file_raw_data):
            if i == 0:
                continue
            line_struc = self._clean_line(line)

            layer = self.lines[int(line_struc[1])]

            for j, value in enumerate(line_struc[3:]):
                kw = f'{layer}_'
                if int(line_struc[1]) < 300 and line_struc[2] != '0':
                    kw += f'tile_{line_struc[2]}_'
                elif int(line_struc[1]) > 300:
                    kw += f'{line_struc[2]}_'
                kw += f'{self.params[j]}'
                file_data[kw] = float(value)
        return file_data

    def create_file(self, ):
        pass
