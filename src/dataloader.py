'''
Dataloader for training
'''
import json
from pathlib import Path
import torch
from readers.readers import AerogelReader, GeometryReader, OpticalReader

class DataLoader():
    '''
    Dataloader object
    '''
    def __init__(self, data_dir, keywords_path):
        '''
        Initialize dataloader to create readers

        Parameters:
            data_dir (str or Path): Path to data directory
        '''
        self.data_dir = Path(data_dir)
        self.aerogel_reader = AerogelReader()
        self.geometry_reader = GeometryReader()
        self.optical_reader = OpticalReader()

        keywords = json.load(open(keywords_path))
        def keywords_reader(keywords):
            return [key for keyword in keywords for key, values in keyword.items() if values["exists"]]

        self.opt_keywords = keywords_reader(keywords['INPUT']['OPTICAL'])
        self.geo_keywords = keywords_reader(keywords['INPUT']['GEOMETRY'])
        self.aer_keywords = keywords_reader(keywords['OUTPUT']['AEROGEL'])

    def get_data(self, geo_name='RichModGeometry.dat', aero_name='RichReco_FastMC.root_hist.root_Aerogel.out', opt_name='RichModOptical.dat'):
        '''
        Load data from the data directory
        '''
        geo_files = self.data_dir.rglob(geo_name)

        dataset_x = []
        dataset_y = []
        i = 0
        for geo_file in geo_files:
            i+=1
            geometry_data = self.geometry_reader(geo_file)
            x_values = [geometry_data[keyword] for keyword in self.geo_keywords]

            if len(self.opt_keywords) > 0:
                opt_file = geo_file.parent.parent / opt_name
                if opt_file.is_file():
                    optical_data = self.optical_reader(opt_file)
                    x_values = x_values + [optical_data[keyword] for keyword in self.opt_keywords]
                else:
                    print("ERROR: Rich Optical file doesn't exist")
            dataset_x.append(x_values)
            aerogel_file = geo_file.parent / aero_name
            aerogel_data = self.aerogel_reader(aerogel_file)
            dataset_y.append([aerogel_data[keyword] for keyword in self.aer_keywords])

        dataset_x = torch.tensor(dataset_x, dtype=torch.float)
        dataset_y = torch.tensor(dataset_y, dtype=torch.float)
        return dataset_x, dataset_y
