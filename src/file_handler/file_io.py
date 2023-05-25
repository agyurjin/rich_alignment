'''
Abstract class for files IO
'''
from abc import ABC
from pathlib import Path

class FileIO(ABC):
    '''
    Abstract class
    '''
    def __init__(self, name=None):
        '''
        Init method
        '''
        self.name = name

    def read_file(self, input_path: Path) -> dict:
        '''
        Read file and parse it to the dict

        Parameters:
            input_path: Path to the input file

        Return:
            Parsed dictinory
        '''
        raise NotImplementedError()

    @staticmethod
    def read_input_file(input_file_path: str) -> list:
        '''
        Read input txt file

        Parameters:
            input_file_path: Path to the data file

        Return:
            raw_data: Input files lines as list
        '''
        with open(input_file_path, encoding="utf8") as file_handler:
            raw_data = file_handler.readlines()
        return raw_data

    def create_file(self, output_path: Path, temp_path: Path, evt_data: dict) -> None:
        '''
        Read template file and create similar file with new parameters

        Parameters:
            output_path: Output file path
            temp_path: Template file path
            evt_data: Data to change in the new file

        Return:
            None
        '''
        raise NotImplementedError()

    @staticmethod
    def _clean_line(line: str) -> list:
        '''
        Split line of the text and clean all unnecessary chrarcters

        Parameters:
            line: Text line to preprocess

        Return:
            line_list: List of the important values from the line
        '''

        line = line.replace('\n','')
        line_split = line.split(' ')
        line_list = [v for v in line_split if v not in ('',' ')]
        return line_list

    def _kw_to_pos(self, keyword: str) -> tuple:
        '''
        Use keyword to find the line and position for change

        Parameters:
            keyword: Parameter to change in the file

        Return:
            Tuple(line number, position number)
        '''
        raise NotImplementedError()
