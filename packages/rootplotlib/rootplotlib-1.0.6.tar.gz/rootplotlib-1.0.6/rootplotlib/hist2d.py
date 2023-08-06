
__all__ = [ 
            #'new',
            #'fill',
            #'density',
            #'divide',
            #'shift',
            ]


from array import array
import rootplotlib as rpl
import ROOT
#import root_numpy
import numpy as np


#
# Create TH1F histogram
#
def new( name, xbins, xmin, xmax, ybins, ymin, ymax, title=''):
    return ROOT.TH2F(name, title, xbins, xmin, xmax, ybins, ymin, ymax)


def new2( name, xbins, ybins, title=''):
    if type(xbins) is list:
        xbins = array('d', xbins)
    elif type(xbins) is np.array:
        xbins = array('d', xbins.tolist())
    if type(ybins) is list:
        ybins = array('d', ybins)
    elif type(xbins) is np.array:
        ybins = array('d', ybins.tolist())
    return ROOT.TH2F(name, title, len(xbins)-1, xbins, len(ybins)-1, ybins)



def fill( hist, xvalues, yvalues ):

    w = array( 'd', np.ones_like( xvalues ) )

    # treat x values
    if type(xvalues) is list:
        xvalues = array('d', xvalues)
    elif (type(xvalues) is np.array) or (type(xvalues) is np.ndarray):
        xvalues = array('d', xvalues.tolist())

    # treat y values
    if type(yvalues) is list:
        yvalues = array('d', yvalues)
    elif (type(xvalues) is np.array) or (type(xvalues) is np.ndarray):
        yvalues = array('d', yvalues.tolist())

    if len(xvalues) != len(yvalues):
        print('It is not possible to fill the histogram. x/y values must be the same size')
    else:
        hist.FillN( len(xvalues), xvalues, yvalues,  w)

    
def density( hist ):
    norm = 1./sum(hist)
    h = hist.Clone()
    h.Reset('M')
    h.SetName( hist.GetName() + '_dens')
    for b in range(0,h.GetNbinsX()+1):
      content = hist.GetBinContent(b)
      value = content*norm
      h.SetBinContent(b , value )
    return h


def divide( hist_num, hist_den ):
    h = hist_num.Clone()
    h.SetName(hist_num.GetName()+'_ratio')
    h.Divide( hist_den )
    return h


def shift( hist, shift_units ):
    h = hist.Clone()
    h.SetName( hist.GetName() + '_shift')
    h.Reset('M')
    for b in range(1, hist.GetNbinsX()):
        content = hist.GetBinContent(b)
        h.SetBinContent(b+shift_units, content)
    return h


def make_hist(name, xaxis_values, yaxis_values, xbins, xmin, xmax, ybins, ymin, ymax):
    '''
    This function will fill a 2D histogram faster than in ROOT and them transform the object into a TH2F in order to make the fit

    Arguments:
    - root_histogram_name: the histogram name for ROOT
    - xaxis_values: the values to be used for fill x-axis
    - yaxis_values: the values to be used for fill y-axis
    - xbin_size: the x-axis bin size
    - ybin_size: the y-axis bin size
    - x_min: the minimum in x-axis
    - x_max: the maximum in x-axis
    - y_min: the minimum in y-axis
    - y_max: the maximum in y-axis
    '''
    
    xbin_size = (xmax - xmin)/xbins    
    ybin_size = (ymax - ymin)/ybins

    # create the bin edges
    binx = np.arange(xmin, xmax, step=xbin_size)
    biny = np.arange(ymin, ymax, step=ybin_size)
    # create a numpy histogram2d
    #H, xedges, yedges = np.histogram2d(x=xaxis_values, y=yaxis_values, bins=(binx, biny))
    # transform into a TH2F
    # create a TH2F to use
    hist = ROOT.TH2F( name, '', len(binx)-1, xmin, xmax, len(biny)-1, ymin, ymax)
    fill(hist, xaxis_values, yaxis_values)
    #return root_numpy.array2hist(H, hist)
    return hist