'''
CERN ROOT plotter
'''
# To skip ROOT pylint errors
#pylint: disable=E1101

import json
from itertools import combinations
from tqdm import tqdm
import torch
import ROOT
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)

class Plotter:
    '''
    Plotter class
    '''
    def __init__(self, model):
        '''
        Init method

        Parameters:
            model: Model for plots
        '''
        self.model = model
        self.in_space = None
        self.out_space = None
        self.min_point = None
        self.stat_error = None
        self.neg_error = None
        self.pos_error = None

    def setup_prediction_plotter(self, in_space, out_space, res):
        '''
        Pass input and output spaces for plots

        Parameters:
            in_space: Input space dict from input JSON
            out_space: Output space dict from input JSON
            res: Results from minimizer
        '''
        self.in_space = in_space
        self.out_space = out_space
        self.min_point = np.array(res['min_point'])
        self.stat_error = np.array(res['stat_error'])
        self.neg_error = np.array(res['neg_error'])
        self.pos_error = np.array(res['pos_error'])

    def create_root_tree(self, output_path):
        '''
        Create ROOT file

        Parameters:
            output_path: ROOT file full path
        '''
        root_file = ROOT.TFile.Open(str(output_path), 'RECREATE')

        N = len(self.min_point)
        if self.in_space['names'][-1] == 'charge':
            N -= 1
        combs = list(combinations(list(range(N)), 2))
        for comb in tqdm(combs):
            axis1 = self.in_space['space'][comb[0]]
            axis2 = self.in_space['space'][comb[1]]
            X = np.tile(self.min_point, axis1[2]*axis2[2]).reshape((axis1[2]*axis2[2],len(self.min_point)))
            axis1_bins = np.linspace(axis1[0],axis1[1],axis1[2])
            axis1_vals = np.repeat(np.linspace(axis1[0],axis1[1],axis1[2]),axis2[2])
            axis2_bins = np.linspace(axis2[0],axis2[1],axis2[2])
            axis2_vals = np.tile(np.linspace(axis2[0],axis2[1],axis2[2]),axis1[2])
            X[:, comb[0]] = axis1_vals
            X[:, comb[1]] = axis2_vals
            X = torch.tensor(X, dtype=torch.float)
            Y = self.model.predict(X)
            Y = Y.detach().numpy()
            Y = np.hstack((Y, Y.sum(axis=1).reshape(len(Y),1)))
            comb = list(comb)
            g1, g2 = self._create_root_tgraph(comb)
            for i in range(Y.shape[1]):
                hist_name = None
                if i == (Y.shape[1]-1):
                    hist_name = 'total'
                else:
                    hist_name = self.out_space['names'][i]
                    continue        
                label = f"{hist_name};{self.in_space['names'][comb[0]]};{self.in_space['names'][comb[1]]}"
                canv_name = '_'.join(label.split(';'))
                canv = ROOT.TCanvas(canv_name, canv_name, 800, 600)
                hist = self._create_root_hist(Y[:, i], X[:, list(comb)], axis1_bins, axis2_bins, label)
                hist.Draw('colz')
                g1.Draw('*')
                g2.Draw('same')
                canv.Write()
        root_file.Close()

    def _create_root_tgraph(self, comb):
        '''
        Create two TGraphs one is for statistics errors, second MINUIT errors

        Parameters:
            comb: Used keywords indexes

        Return:
            g1: Statistics errors TGraph
            g2: MINUIT errors TGraph
        '''
        min_point = self.min_point[comb]
        min_error = self.stat_error[comb]
        pos_error = self.pos_error[comb]
        neg_error = self.neg_error[comb]

        x =  np.array(min_point[0], dtype=np.float32)
        y = np.array(min_point[1], dtype=np.float32)
        ex = np.array(min_error[0], dtype=np.float32)
        ey = np.array(min_error[1], dtype=np.float32)
        g1 = ROOT.TGraphErrors(1, x, y, ex, ey)
        g1.SetMarkerColor(2)

        exl = np.array(neg_error[0], dtype=np.float32)
        exh = np.array(pos_error[0], dtype=np.float32)
        eyl = np.array(neg_error[1], dtype=np.float32)
        eyh = np.array(pos_error[1], dtype=np.float32)
        g2 = ROOT.TGraphAsymmErrors(1, x, y, exl, exh, eyl, eyh)
        g2.SetMarkerColor(6)
        g2.SetMarkerStyle(21)

        return g1, g2

    @staticmethod
    def _create_root_hist(chi2, points, axis1_bins, axis2_bins, labels=None):
        '''
        Create single plot

        Parameters:
            chi2 (numpy.array or torch.tensor): Chi square value for each point
            points (numpy.array or torch.tensor): Data points
            labels (str): Name and axis titles for the plot
            fn (str): Output file path
            mins (np.array): Calculated minima point for the model
            min_error (np.array): Error calculation from convergence
            pos_error (list): Positive error from MINUIT error calculation
            neg_error (list): Negative error from MINUIT error calculation
        '''
        hist_name = '_'.join(labels.split(';'))
        axis_x = set(list(axis1_bins))
        axis_y = set(list(axis2_bins))
        xbin = (max(axis_x) - min(axis_x))/(len(axis_x)-1)
        ybin = (max(axis_y) - min(axis_y))/(len(axis_y)-1)
        hist = ROOT.TH2F(hist_name, hist_name, len(axis_x), min(axis_x)-xbin/2, max(axis_x)+xbin/2, len(axis_y), min(axis_y)-ybin/2, max(axis_y)+ybin/2)
        for point, c2 in zip(points,chi2):
            xidx = int((point[0] - min(axis_x))/xbin + xbin/2)+1
            yidx = int((point[1] - min(axis_y))/ybin + ybin/2)+1
            hist.SetBinContent(xidx, yidx, c2)
        hist.SetTitleOffset(1.5, "Y")
        hist.SetTitle(labels)
        return hist

    @staticmethod
    def draw_losses(output_path, loss_hist_name):
        '''
        Draw training loss function from saved JSON file

        Parameters:
            output_path: Loss history JSON path
            loss_hist_name: Name of the file
        '''
        with open(output_path / loss_hist_name, encoding='utf8') as file_handler:
            loss_data = json.load(file_handler)
        canv = ROOT.TCanvas('canv', 'canv', 800, 600)
        epochs = np.array(loss_data['epochs'], dtype=float)
        train = np.array(loss_data['train_loss'], dtype=float)
        test = np.array(loss_data['val_loss'], dtype=float)
        N = len(epochs)
        if N <1:
            return
        g1 = ROOT.TGraph(N, epochs, train)
        g2 = ROOT.TGraph(N, epochs, test)

        g2.SetLineColor(2)

        mg = ROOT.TMultiGraph()
        mg.Add(g1)
        mg.Add(g2)
        mg.Draw('AC')
        mg.SetTitle('Training vs Validation history;Epochs;Average RMS/points')
        leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
        leg.AddEntry(g1, 'train history', 'l')
        leg.AddEntry(g2, 'val history', 'l')
        leg.Draw()
        canv.SetLogy()
        output_path = output_path / 'loss.pdf'
        canv.SaveAs(str(output_path))

    def draw_diff(self, output_path, data_reader):
        '''
        Draw absoulute and relative differences

        Parameters:
            output_path: Output path to save figure
            data_reader: DataReader object
        '''
        canv = ROOT.TCanvas('canv', 'canv', 800, 600)
        h1 = ROOT.TH1F('h1', 'h1', 400, -0.5, 0.5)
        h2 = ROOT.TH1F('h2', 'h2', 400, -0.5, 0.5)

#        train_loader, val_loader, _ = data_reader.get_data(240, norm=False)
#        X_train, y_train = next(iter(train_loader))
#        X_val , y_val = next(iter(val_loader))
        X_train, X_val, y_train, y_val = data_reader.get_data(240, norm=False)
        y_train_pred = self.model.predict(X_train)
        y_val_pred = self.model.predict(X_val)

        y_train_pred = y_train_pred.mean(axis=1)
        y_val_pred = y_val_pred.mean(axis=1)
        y_train = y_train.mean(axis=1)
        y_val = y_val.mean(axis=1)

        for y_p, y in zip(y_train_pred, y_train):
            h1.Fill(y_p - y)
            h2.Fill((y_p - y)/y)

        h2.SetLineColor(2)
        h2.Draw()
        h2.SetTitle('Model vs data;(chi2_average_pred - chi2_average_real);count')
        leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
        leg.AddEntry(h1, 'absolute', 'l')
        leg.AddEntry(h2, 'relative', 'l')
        h1.Draw('same')
        leg.Draw()
        canv.SaveAs(str(output_path))
