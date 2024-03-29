'''
NN model
'''
import json
from copy import deepcopy
import torch
from pathlib import Path
from .base_model import BaseModel
from .nets import fcn
from torch.utils.data import Dataset, DataLoader

class NNModel(BaseModel):
    '''
    Neural Network model class
    '''
    def __init__(self, configs):
        '''
        Create object with configs

        Parameters:
            configs (dict): Configs to create model, training values

        Return:
            None
        '''
        super().__init__()
        self.model = fcn(configs)
        self.loss_hist = {'train_loss': [], 'val_loss':[], 'epochs':[]}
        self.norm_params = {'x_mean': [], 'x_std': [], 'y_mean': [], 'y_std': []}
        self.device = 'cpu'#'cuda' if torch.cuda.is_available() else 'cpu'

    def train(self, data_reader, train_info):
        lr = train_info['optimizer']['lr']
        momentum = train_info['optimizer']['momentum']

        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=lr, momentum=momentum)

        #optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        running_loss = 0
        best_model = None
        best_loss = 1e10
        verbose = 1000

        x_train, x_val, y_train, y_val = data_reader.get_data(val_size=train_info['val_size'],norm=False)

        x_train_mean = x_train.mean(axis=0)
        y_train_mean = y_train.mean(axis=0)
        x_train_std = x_train.std(axis=0)
        y_train_std = y_train.std(axis=0)


        self.norm_params['x_mean'] = x_train_mean
        self.norm_params['x_std'] = x_train_std
        self.norm_params['y_mean'] = y_train_mean
        self.norm_params['y_std'] = y_train_std

        x_train = (x_train - x_train_mean)/(x_train_std+1e-5)
        y_train = (y_train - y_train_mean)/(y_train_std+1e-5)
        x_val = (x_val - x_train_mean)/(x_train_std+1e-5)
        y_val = (y_val - y_train_mean)/(y_train_std+1e-5)

        x_train, x_val = x_train.to(self.device), x_val.to(self.device)
        y_train, y_val = y_train.to(self.device), y_val.to(self.device)

        print(x_train.shape)
        print(y_train.shape)

#        train_loader, val_loader, self.norm_params = \
#data_reader.get_data(train_info['batch_size'], train_info['val_size'], train_info['norm'])

        self.model = self.model.to(self.device)
        batch_size = data_reader.batch_size
        num_of_batches = data_reader.num_of_batches

#        train_loader = DataLoader(list(zip(x_train,y_train)), shuffle=True, batch_size=batch_size)

        for i in range(train_info['epochs']):
            optimizer.zero_grad()
            y_pred = self.model(x_train)
            loss_v = loss_fn(y_pred, y_train)
            loss_v.backward()
            optimizer.step()
            running_loss += float(loss_v)

#            for _ in range(num_of_batches):
#                x_train, y_train = next(iter(train_loader))
#                optimizer.zero_grad()
#                y_pred = self.model(x_train)
#                loss_v = loss_fn(y_pred, y_train)
#                loss_v.backward()
#                optimizer.step()
#                running_loss += float(loss_v)

            if (i+1) % verbose == 0:
                with torch.no_grad():
                    y_pred = self.model(x_val)
                    loss_v = loss_fn(y_pred, y_val)
                    val_loss = float(loss_v)
                if val_loss < best_loss:
                    best_model = deepcopy(self.model)
                    best_loss = val_loss

                print('*'*20)
                print(f"[TRAINING] Epoch {i+1}/{train_info['epochs']}")
                print(f'[TRAINING] train loss: {running_loss/verbose:.5f}')
                print(f'[TRAINING] val loss: {val_loss:.5f}')
                print('*'*20)
                self.loss_hist['train_loss'].append(running_loss/verbose/num_of_batches)
                self.loss_hist['val_loss'].append(val_loss)
                self.loss_hist['epochs'].append(i+1)

#                if (i+1) % (verbose*10) == 0:
#                    output_dir = Path(f'model_{i+1}')
#                    output_dir.mkdir(exist_ok=True, parents=True)
#                    self.save_model(output_dir)
                running_loss = 0

        if best_model is not None:
            self.model = best_model

    def predict(self, x: torch.tensor) -> torch.tensor:
        '''
        Predict value for the given points

        Parameters:
            x: Points for prediction

        Return:
            y_pred: Predicted values
        '''
        x = (x - self.norm_params['x_mean'])/self.norm_params['x_std']
        with torch.no_grad():
            y_pred = self.model.to('cpu')(x)
        y_pred = y_pred * self.norm_params['y_std'] + self.norm_params['y_mean']
        return y_pred

    def save_model(self, output_path):
        '''
        Save model state to the file.

        Parameters:
            output_path : Path were the model weights will be saved.

        Return:
            None
        '''
        model_name = 'model.pth'
        model_config_name = 'model_config.json'
        loss_hist_name = 'loss_hist.json'

        res = {}
        res['x_mean'] = self.norm_params['x_mean'].tolist()
        res['x_std'] = self.norm_params['x_std'].tolist()
        res['y_mean'] = self.norm_params['y_mean'].tolist()
        res['y_std'] = self.norm_params['y_std'].tolist()

        torch.save(self.model.state_dict(), output_path/model_name)
        with open(output_path/loss_hist_name, 'w', encoding='utf8') as fw:
            json.dump(self.loss_hist, fw)

        with open(output_path/model_config_name, 'w', encoding='utf8') as fw:
            json.dump(res, fw)

        res = {
            'model_name': model_name,
            'model_config_name': model_config_name,
            'loss_hist_name': loss_hist_name
        }
        return res

    def load_model(self, model_path, norm_path):
        '''
        Load model from the path

        Parameters:
            model_path : Path to the model weights should be loaded.

        Return:
            None
        '''
        self.model.load_state_dict(torch.load(model_path))
        with open(norm_path, encoding='utf8') as file_handler:
            norm_data = json.load(file_handler)
        x_mean = torch.tensor(norm_data['x_mean'])
        x_std = torch.tensor(norm_data['x_std'])
        y_mean = torch.tensor(norm_data['y_mean'])
        y_std = torch.tensor(norm_data['y_std'])
        self.norm_params = {'x_mean': x_mean, 'x_std': x_std, 'y_mean': y_mean, 'y_std': y_std}
