'''
'''
import time
import json
from pathlib import Path
import shutil


from .data_handler import DataGenerator, DataLoader
from .models import RICHAlignmentModel
from .minimizers import Minimizer
from .plotter import Plotter


class RICHAlignment():
    def __init__(self, jsons_dir='jsons'):
        self.input_jsons_dir = Path(jsons_dir) if isinstance(jsons_dir, str) else jsons_dir

    def run_training(self, output_dir):
        train_meta_data = json.load(open(self.input_jsons_dir/'training_config.json'))
        keywords_path = self.input_jsons_dir / train_meta_data['META']['keywords_name']
        raw_keywords = json.load(open(keywords_path))

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True) 
        
        if train_meta_data['DATASETS']['neg_pos_mixing'] not in ('average', 'free', 'charge'):
            print('ERROR: data mixing is wrong in json file!!!!!!!')
        if train_meta_data['DATASETS']['charge'] not in ('positive', 'negative', 'mixed'):
            print('ERROR: charge is wrong in json file!!!!!!!!!!!')

        data_loader = DataLoader(raw_keywords, train_meta_data['META'], train_meta_data['DATASETS'])

        split_ratio = train_meta_data['TRAINING']['split_ratio']
        batch_size = train_meta_data['TRAINING']['batch_size']
        shuffle = train_meta_data['TRAINING']['shuffle']
        data_loader.split_data(split_ratio, batch_size, shuffle)

        train_meta_data['MODEL']['input_layer'] = data_loader.in_dim
        train_meta_data['MODEL']['output_layer'] = data_loader.out_dim
 
        model = RICHAlignmentModel(train_meta_data['MODEL'])
        epochs = train_meta_data['TRAINING']['epochs']
            
        res = model.train(output_dir, data_loader, train_meta_data['TRAINING']['epochs'], train_meta_data['TRAINING']['optimizer'])
        
        shutil.copy(keywords_path, output_dir/ train_meta_data['META']['keywords_name'])
        with open(output_dir / 'training_config.json', 'w') as fw:
            json.dump(train_meta_data, fw, indent=2)

        plots = Plotter(model)
        plots.draw_losses(output_dir, res['loss_hist_name'])
        plots.draw_diff(output_dir/'diff.pdf', data_loader)
                
    def run_prediction(self, trained_model_dir):
        trained_model_dir = Path(trained_model_dir)
        train_data = json.load(open(trained_model_dir / 'training_config.json'))
        model = RICHAlignmentModel(train_data['MODEL'])
        model.load_model(trained_model_dir/'model.pth', trained_model_dir/'model_config.json')

        minima_data = json.load(open(self.input_jsons_dir/'minima_config.json'))

        mixing=None        
        if train_data['DATASETS']['charge'] == 'mixed':
            mixing = train_data['DATASETS']['neg_pos_mixing']

        keywords_path = self.input_jsons_dir / train_data['META']['keywords_name']
        raw_keywords = json.load(open(keywords_path))
        in_space, out_space = self._create_workspace(raw_keywords, minima_data['MINIMA']['precisions'], mixing)

        minimizer = Minimizer(model, minima_data)
        min_point, min_error, pos_error, neg_error = minimizer.find_minima(in_space)

        res = {
            'min_point': list(min_point),
            'stat_error': list(min_error),
            'neg_error': list(neg_error),
            'pos_error': list(pos_error)
            }

        with open(trained_model_dir / 'results.json', 'w') as fw:
            json.dump(res, fw, indent=2)

        plots = Plotter(model)
        plots.setup_prediction_plotter(in_space, out_space, res)
        root_path = trained_model_dir / 'plots.root'
        plots.create_root_tree(root_path)


    def create_data(self, output_dir: str or Path, number_of_points: int, \
        geo_path=None, opt_path=None) -> None:
 
        if isinstance(geo_path, str):
            geo_path = Path(geo_path)
        if isinstance(opt_path, str):
            opt_path = Path(opt_path)
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        keywords_data = json.load(open(self.input_jsons_dir / 'keywords.json'))
        template_path = {'geo': geo_path, 'opt': opt_path}

        data_gen = DataGenerator(keywords_data['INPUT'], template_path)
        data_gen.create(output_dir, number_of_points)

    def _create_workspace(self, keywords, precisions, mixing):
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

        output_keywords = keywords['OUTPUT']['AEROGEL']
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

    def _timestamp(self):
        return time.strftime('%d:%m:%Y::%H:%M:%S')
