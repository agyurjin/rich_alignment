'''
RICH Alignment object to train model and find best alignment parameters
'''
import json
from pathlib import Path
import shutil
from typing import Tuple
import logging

from .data_handler import DataGenerator, DataReader
from .models import RICHAlignmentModel
from .minimizers import Minimizer
from .plotter import Plotter
#from .verifier import Verifier

class RICHAlignment():
    '''
    Class to use input JSONS to setup.
    '''
    def __init__(self, jsons_dir='jsons'):
        '''
        Init method

        Parameters:
            jsons_dir (str): Input JSONS dir

        Return:
            None
        '''
        self.input_jsons_dir = Path(jsons_dir) if isinstance(jsons_dir, str) else jsons_dir
#        self.verifier = Verifier()        

    def test_verif(self):
        with open(self.input_jsons_dir/'keywords.json', encoding='utf8') as file_handler:
            kw_data = json.load(file_handler)
        self.verifier.start(kw_data)

    def run_training(self, output_dir: str) -> None:
        """
        Use input JSONS to train model

        Parameters:
            output_dir (str): Folder dir to save model outputs
        """
        with open(self.input_jsons_dir/'training_config.json', encoding='utf8') as file_handler:
            train_meta_data = json.load(file_handler)
        keywords_path = self.input_jsons_dir / train_meta_data['META']['keywords_name']
        with open(keywords_path, encoding='utf8') as file_handler:
            raw_keywords = json.load(file_handler)

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)

        if train_meta_data['DATASETS']['neg_pos_mixing'] not in ('average', 'free', 'charge'):
            print('ERROR: data mixing is wrong in json file!!!!!!!')
        if train_meta_data['DATASETS']['charge'] not in ('positive', 'negative', 'mixed'):
            print('ERROR: charge is wrong in json file!!!!!!!!!!!')

        data_reader = DataReader(raw_keywords, train_meta_data['META'], train_meta_data['DATASETS'])
        
        train_meta_data['MODEL']['input_layer'] = data_reader.in_dim
        train_meta_data['MODEL']['output_layer'] = data_reader.out_dim

        model = RICHAlignmentModel(train_meta_data['MODEL'])

        res = model.train(output_dir, data_reader, train_meta_data['TRAINING'])

        shutil.copy(keywords_path, output_dir/ train_meta_data['META']['keywords_name'])
        with open(output_dir/'training_config.json', 'w', encoding='utf8') as fw:
            json.dump(train_meta_data, fw, indent=2)

        plots = Plotter(model)
        plots.draw_losses(output_dir, res['loss_hist_name'])
        plots.draw_diff(output_dir/'diff.pdf', data_reader)  

    def run_minimum_finder(self, trained_model_dir: str) -> None:
        '''
        Use trained model and input JSONs to find best alignment parameters

        Parameters:
            trained_model_dir (str): Trained model directory path

        Return:
            None
        '''
        trained_model_dir = Path(trained_model_dir)
        with open(trained_model_dir/'training_config.json', encoding='utf8') as file_handler:
            train_data = json.load(file_handler)

        model = RICHAlignmentModel(train_data['MODEL'])
        model.load_model(trained_model_dir/'model.pth', trained_model_dir/'model_config.json')

        with open(self.input_jsons_dir/'minima_config.json',encoding='utf8') as file_handler:
            minima_data = json.load(file_handler)

        mixing=None
        if train_data['DATASETS']['charge'] == 'mixed':
            mixing = train_data['DATASETS']['neg_pos_mixing']

        keywords_path = self.input_jsons_dir / train_data['META']['keywords_name']
        with open(keywords_path, encoding='utf8') as file_handler:
            raw_keywords = json.load(file_handler)

        in_space, out_space = self._create_workspace(raw_keywords, \
minima_data['MINIMA']['precisions'], mixing)

        minimizer = Minimizer(model, minima_data)
        min_point, min_error, pos_error, neg_error = minimizer.find_minima(in_space)

        res = {
            'min_point': list(min_point),
            'stat_error': list(min_error),
            'neg_error': list(neg_error),
            'pos_error': list(pos_error)
            }

        with open(trained_model_dir/'results.json', 'w', encoding='utf8') as fw:
            json.dump(res, fw, indent=2)

        plots = Plotter(model)
        plots.setup_prediction_plotter(in_space, out_space, res)
        root_path = trained_model_dir / 'plots.root'
        plots.create_root_tree(root_path)


    def create_data(self, output_dir: str or Path, number_of_points: int, \
        geo_path=None, opt_path=None) -> None:
        '''
        Creates data points similar to templates that are used for RICH Fast Monte
        Carlo simulation

        Parameters:
            output_dir: Directory to create RICH alignment combinations
            number_of_point: Number of alignment combinations to create
            geo_path: Geometry template file path
            opt_path: Optical template file path
        '''

        if isinstance(geo_path, str):
            geo_path = Path(geo_path)
        if isinstance(opt_path, str):
            opt_path = Path(opt_path)
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        with open(self.input_jsons_dir/'keywords.json', encoding='utf8') as file_handler:
            keywords_data = json.load(file_handler)
        template_path = {'geo': geo_path, 'opt': opt_path}

        data_gen = DataGenerator(keywords_data['INPUT'], template_path)
        data_gen.create(output_dir, number_of_points)

    @staticmethod
    def _create_workspace(keywords:dict, precisions:dict, mixing:str)->Tuple[dict]:
        '''
        Create input space with keywords names preciisions, and data structure

        Pparameters:
            keywords: Input and Output keywords for model training
            precisions: Steps for each input feature group
            mixing: Can be (average, free, charge). Different methods to take
                account positive and negative parts.

        Return:
            in_space: Input space from keywords, precisions and space values
            out_space: Output space keywords names
        '''
        in_space = {'space': [], 'names': [], 'precisions': []}
        out_space = {'names': []}

        input_keywords = keywords['INPUT']['GEOMETRY'] + keywords['INPUT']['OPTICAL']
        for inkw in input_keywords:
            for name, value in inkw.items():
                if value['exists']:
                    in_space['space'].append(value['grid'])
                    in_space['names'].append(name)
                    feature_is = 'distance'
                    if name.find('theta') > 0:
                        feature_is = 'angle'
                    elif name.find('ref_index') > 0:
                        feature_is = 'ref_index'
                    in_space['precisions'].append(precisions[feature_is])

        if mixing == 'charge':
            in_space['space'].append([0,1,1])
            in_space['names'].append('charge')
            in_space['precisions'].append(1)

        output_keywords = keywords['OUTPUT']['AEROGEL'] + keywords['OUTPUT']['TOPOLOGY'] + keywords['OUTPUT']['MAPMT'] + keywords['OUTPUT']['TRACKS']
        names = []
        for outkw in output_keywords:
            for name, value in outkw.items():
                if value['exists']:
                    names.append(name)

        if mixing == 'free':
            neg_names = [f'neg_{name}' for name in names]
            pos_names = [f'pos_{name}' for name in names]
            out_space['names'] = neg_names + pos_names
        else:
            out_space['names'] = names

        return in_space, out_space
