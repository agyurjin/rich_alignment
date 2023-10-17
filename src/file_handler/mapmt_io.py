from pathlib import Path

from .file_io import FileIO
from .reader_structs import AERO_FILE_PARAMS

class MapmtIO(FileIO):
    def __init__(self, name=None):
        super().__init__(name)
        self.params = AERO_FILE_PARAMS

    def read_file(self, input_path: Path) -> dict:
        file_raw_data = self.read_input_file(input_path)
        file_data = {}
        for line in file_raw_data:
            line_struc = self._clean_line(line)
            for j, value in enumerate(line_struc):
                key = f'mapmt_{self.params[j]}'
                file_data[key] = float(value)
        return file_data


    def create_file(self, output_path: Path, tmep_path: Path, evt_data: dict) -> None:
        raise NotImplementedError('Aerogel file creation method not implemented \
as it should be generated from simulations!')
