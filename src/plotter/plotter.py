import ROOT
import numpy as np
from itertools import combinations
import torch
from tqdm import tqdm
import json

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)

class Plotter:
    def __init__(self, model):
        self.model = model
        self.in_space = None
        self.out_space = None
        self.min_point = None
        self.stat_error = None
        self.neg_error = None
        self.pos_error = None

    def setup_prediction_plotter(self, in_space, out_space, res):
        self.in_space = in_space
        self.out_space = out_space
        self.min_point = np.array(res['min_point'])
        self.stat_error = np.array(res['stat_error'])
        self.neg_error = np.array(res['neg_error'])
        self.pos_error = np.array(res['pos_error'])

    def create_root_tree(self, output_path):
        root_file = ROOT.TFile.Open(str(output_path), 'RECREATE')

        combs = list(combinations(list(range(len(self.min_point))), 2))
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
            Y = np.hstack((Y, Y.mean(axis=1).reshape(len(Y),1)))

            comb = list(comb)
            g1, g2 = self._create_root_tgraph(comb)
            for i in range(Y.shape[1]):
                hist_name = None
                if i == (Y.shape[1]-1):
                    hist_name = 'total'
                else:
                    hist_name = self.out_space['names'][i]
                label = f"{hist_name};{self.in_space['names'][comb[0]]};{self.in_space['names'][comb[1]]}"
                canv_name = '_'.join(label.split(';'))
                canv = ROOT.TCanvas(canv_name, canv_name, 800, 600)
                hist = self._create_root_hist(Y[:, i], X[:, list(comb)], axis1_bins, axis2_bins, label)
                hist.Draw('colz')
                g1.Draw('*')
                g2.Draw('same')
                canv.Write()

    def _create_root_tgraph(self, comb):
        min_point = self.min_point[comb]
        min_error = self.stat_error[comb]
        pos_error = self.pos_error[comb]
        neg_error = self.neg_error[comb]

        x =  np.array(min_point[0], dtype=np.float)
        y = np.array(min_point[1], dtype=np.float)
        ex = np.array(min_error[0], dtype=np.float)
        ey = np.array(min_error[1], dtype=np.float)
        g1 = ROOT.TGraphErrors(1, x, y, ex, ey)
        g1.SetMarkerColor(2)

        exl = np.array(neg_error[0], dtype=np.float)
        exh = np.array(pos_error[0], dtype=np.float)
        eyl = np.array(neg_error[1], dtype=np.float)
        eyh = np.array(pos_error[1], dtype=np.float)
        g2 = ROOT.TGraphAsymmErrors(1, x, y, exl, exh, eyl, eyh)
        g2.SetMarkerColor(6)
        g2.SetMarkerStyle(21)

        return g1, g2

    def _create_root_hist(self, chi2, points, axis1_bins, axis2_bins, labels=None):
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

    def draw_losses(self, output_path, loss_hist_name):
        loss_data = json.load(open(output_path / loss_hist_name))
        canv = ROOT.TCanvas('canv', 'canv', 800, 600)
        epochs = np.array(loss_data['epochs'], dtype=float)
        train = np.array(loss_data['train_loss'], dtype=float)
        test = np.array(loss_data['val_loss'], dtype=float) 
        N = len(epochs)
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


    def draw_diff(self, output_path, data_loader):
        canv = ROOT.TCanvas('canv', 'canv', 800, 600)
        h1 = ROOT.TH1F('h1', 'h1', 40, -0.6, 0.6)
        h2 = ROOT.TH1F('h2', 'h2', 40, -0.6, 0.6)

        X_train, y_train = data_loader.get_trainset()
        X_val, y_val = data_loader.get_testset()
        
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
