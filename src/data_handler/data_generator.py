
import sys
import numpy as np
import json
import ROOT
from array import array
from pathlib import Path

from ..file_handler import DataParser

class DataGenerator():
    def __init__(self, input_dict: dict, temp_paths: dict) -> None: 
        self.data_parser = DataParser()

        self.geo_keywords = []
        self.opt_keywords = []
        self.input_dict = {}
        for i, keywords in enumerate([input_dict['GEOMETRY'], input_dict['OPTICAL']]):
            for keyword in keywords:
                key, values = list(keyword.items())[0]
                if values['exists']:
                    if i == 0:
                        self.geo_keywords.append(key)
                    else:
                        self.opt_keywords.append(key)        
                    self.input_dict[key] = values['grid']

        self.geo_temp_path, self.opt_temp_path = None, None    
        if 'geo' in temp_paths:
            self.geo_temp_path = temp_paths['geo']
        if 'opt' in temp_paths:
            self.opt_temp_path = temp_paths['opt']

        self._logs('geometry')
        self._logs('optical')

    def _logs(self, file_type):
        keywords, temp_path = None, None
        if file_type == 'geometry':
            keywords, temp_path = self.geo_keywords, self.geo_temp_path
        else:
            keywords, temp_path = self.opt_keywords, self.opt_temp_path

        if len(keywords) == 0 and temp_path:
            print(f'WARNING: all {file_type} files are same. No selceted keywords in keyword.json')
        elif len(keywords) == 0 and not temp_path:
            print(f'NOTE: {file_type} data will not be generated!')
        elif len(keywords) != 0 and temp_path:
            print(f'NOTE: {file_type} data will be generated!')
        else:
            print(f'ERROR: {file_type} template file is not provied!!!')


    def create(self, output_dir: Path, num_of_points: int) -> None:
        geo_dir = output_dir / 'geo'
        opt_dir = output_dir / 'opt'
        geo_dir.mkdir(exist_ok=True, parents=True)
        opt_dir.mkdir(exist_ok=True)

        root_path = output_dir / 'data.root'

        root_file = ROOT.TFile.Open(str(root_path), 'RECREATE')
        tree = ROOT.TTree('evtTree', 'Generated data tree')

        single_event = []
        keywords = self.geo_keywords + self.opt_keywords
        for i, key in enumerate(keywords):
            single_event.append(array('d',[0]))
            tree.Branch(key, single_event[i], key+'/D')

        for i in range(num_of_points):
            geo_event, opt_event = self._generate_event()
            if self.geo_temp_path:
                self._create_file(geo_dir, geo_event, i)
            if self.opt_temp_path:
                self._create_file(opt_dir, opt_event, i)

            for idx, keyword in enumerate(keywords):
                value = geo_event[keyword] if keyword in geo_event else opt_event[keyword]
                single_event[idx][0] = value
            tree.Fill()
        tree.Write()
    
    def _generate_event(self) -> tuple:
        geo_event = {}
        opt_event = {}
        for i, keywords in enumerate([self.geo_keywords, self.opt_keywords]):
            for keyword in keywords:
                grid = self.input_dict[keyword]
                value = np.random.uniform(grid[0], grid[1])
                if i == 0:
                    geo_event[keyword] = value
                else:
                    opt_event[keyword] = value
        return geo_event, opt_event

    def _create_file(self, in_dir: Path, event: dict, idx: int):
        file_path, temp_path = None, None 
        if in_dir.name =='geo':
            file_path = in_dir / f'{self.geo_temp_path.stem}_{idx}{self.geo_temp_path.suffix}'
            temp_path = self.geo_temp_path
        else:
            file_path = in_dir / f'{self.opt_temp_path.stem}_{idx}{self.opt_temp_path.suffix}'
            temp_path = self.opt_temp_path

        self.data_parser.create_file(file_path, temp_path, event)
        
