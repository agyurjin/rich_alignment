from pathlib import Path

from .file_io import FileIO
from .reader_structs import TRACKS_PARAMS


class TracksIO(FileIO):
    def __init__(self, name=None):
        super().__init__(name)
        self.params = TRACKS_PARAMS

    def read_file(self, input_path):
        file_raw_data = self.read_input_file(input_path)
        file_data = {}
        for line in file_raw_data:
            line_struc = self._clean_line(line)
            pmt_id = line_struc[0]
            for j,value in enumerate(line_struc[1:]):
                key = f'track_pmt_{pmt_id}_{self.params[j]}'
                file_data[key] = float(value)
        return file_data


    def create_file(self, output_path, temp_path, evt_data):
        raise NotImplementedError('Error')
