'''
Run training
'''
import json
from pathlib import Path

from dataloader import DataLoader
from trainer import Trainer

from plotters import create_plots
from utils import get_keyword_names

def main():
    '''
    Run main function
    '''

    config_path = 'training_config.json'
    configs = json.load(open(config_path))

    data_loader = DataLoader(configs['PATHS']['dataset_path'], configs['PATHS']['keywords_path'])
    X, Y = data_loader.get_data(aero_name='RichReco_FastMC.root_hist.root_hm_Aerogel.out')
    if X.shape[1] <= 2:
        keywords = json.load(open(configs['PATHS']['keywords_path']))
        in_kw_names, out_kw_names = get_keyword_names(keywords)
        kw_names = {'in_kw_names': in_kw_names, 'out_kw_names': out_kw_names}

        out_path = Path(configs['PATHS']['output_path']) / 'train.pdf'
        create_plots(Y.detach().numpy(), X.detach().numpy(), str(out_path), kw_names)
    configs['MODEL']['input_layer'] = X.size()[1]
    configs['MODEL']['output_layer'] = Y.size()[1]
    model_trainer = Trainer(configs)
    print("MODEL TRAINING STARTED ...")
    model_trainer.train(X,Y)


if __name__ == '__main__':
    main()
