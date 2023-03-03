'''
Useful functions for plotting with ROOT
'''
import numpy as np
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)

def create_plots(Y, X, out_path, kw_names=None, mins=None, min_error=None, pos_error=None, neg_error=None):
    '''
    Create all plots

    Parameters:
        Y (np.array or torch.tensor): Model output data
        X (np.array or torch.tensor): Model input data
        out_path (str): Output file path
        kw_names (list): All input keywrods names that exists is True
        mins (np.array): Calculated minima point for the model
        min_error (np.array): Error calculation from convergence
        pos_error (list): Positive error from MINUIT error calculation
        neg_error (list): Negative error from MINUIT error calculation

    '''
    in_kw_names = kw_names['in_kw_names']
    out_kw_names = kw_names['out_kw_names']
    labels = ['total chi2;{};{}'.format(*in_kw_names)]
    for kw_name in out_kw_names:
        labels.append('{};{};{}'.format(kw_name, *in_kw_names))
    for i, label in enumerate(labels):
        y = Y.sum(axis=1) if i == 0 else Y[:, i-1]
        fn = out_path
        if i == 0:
            fn = out_path + '('
        elif i == (len(labels) - 1):
            fn = out_path + ')'
        _plot_single(y, X, label, fn, mins, min_error, pos_error, neg_error)
    projection_x(y,X)

def _plot_single(chi2, points, labels, fn, mins, min_error, pos_error, neg_error):
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
    canv = ROOT.TCanvas('canv', 'canv', 800, 600)

    axis_x = set(points[:, 0])
    axis_y = set(points[:, 1])
    xbin = (max(axis_x) - min(axis_x))/(len(axis_x)-1)
    ybin = (max(axis_y) - min(axis_y))/(len(axis_y)-1)
    hist = ROOT.TH2F('hist', 'hist', len(axis_x), min(axis_x)-xbin/2, max(axis_x)+xbin/2, len(axis_y), min(axis_y)-ybin/2, max(axis_y)+ybin/2)
    for point, c2 in zip(points,chi2):
        xidx = int((point[0] - min(axis_x))/xbin + xbin/2)+1
        yidx = int((point[1] - min(axis_y))/ybin + ybin/2)+1
        hist.SetBinContent(xidx, yidx, c2)
    hist.SetTitleOffset(1.5,"Y")
    hist.SetTitle(labels)
    hist.Draw('colz')

    if mins is not None:
        x =  np.array(mins[0], dtype=np.float)
        y = np.array(mins[1], dtype=np.float)
        ex = np.array(min_error[0], dtype=np.float)
        ey = np.array(min_error[1], dtype=np.float)
        g1 = ROOT.TGraphErrors(1, x, y, ex, ey)
        g1.SetMarkerColor(2)
        g1.Draw('*')

        exl = np.array(neg_error[0], dtype=np.float)
        exh = np.array(pos_error[0], dtype=np.float)
        eyl = np.array(neg_error[1], dtype=np.float)
        eyh = np.array(pos_error[1], dtype=np.float)
        g2 = ROOT.TGraphAsymmErrors(1, x, y, exl, exh, eyl, eyh)
        g2.SetMarkerColor(6)
        g2.SetMarkerStyle(21)
        g2.Draw('same')

    canv.SaveAs(fn)

def projection_x(chi2, points):
    canv = ROOT.TCanvas('canv', 'canv', 800, 600)
    gr = ROOT.TGraph(len(chi2), np.array(points[:,1], dtype=float),  np.array(chi2,dtype=float))
    gr.Draw('AP*')
    canv.SaveAs('test.pdf')
