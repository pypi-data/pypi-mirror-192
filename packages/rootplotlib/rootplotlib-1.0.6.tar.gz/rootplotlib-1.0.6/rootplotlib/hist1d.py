
__all__ = [ 
            #'new',
            #'fill',
            #'density',
            #'divide',
            #'shift',
            ]


import array
import rootplotlib as rpl
import ROOT
import numpy as np


#
# Create TH1F histogram
#
def new( name, bins, xmin, xmax, title=''):
    return ROOT.TH1F(name, title, bins, xmin, xmax)


def new2( name, xbins, title=''):
    if type(xbins) is list:
        xbins = array('d', xbins)
    elif type(xbins) is np.array:
        xbins = array('d', xbins.tolist())
    return ROOT.TH1F(name, title, len(xbins), xbins)


def fill( hist, values ):
    w = array.array( 'd', np.ones_like( values ) )
    hist.FillN( len(values), array.array('d',  values),  w)

    
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
    hist = hist_num.Clone()
    hist.SetName(hist_num.GetName()+'_ratio')
    hist.Divide( hist_num, hist_den,1.,1.,'B' )
    return hist


def shift( hist, shift_units ):
    h = hist.Clone()
    h.SetName( hist.GetName() + '_shift')
    h.Reset('M')
    for b in range(1, hist.GetNbinsX()):
        content = hist.GetBinContent(b)
        h.SetBinContent(b+shift_units, content)
    return h



def rebin( hist, nbins, xmin, xmax ):
  h = ROOT.TH1F(hist.GetName()+'_resize', hist.GetTitle(), nbins,xmin,xmax)
  for bin in range(h.GetNbinsX()):
    x = h.GetBinCenter(bin+1)
    m_bin = hist.FindBin(x)
    y = hist.GetBinContent(m_bin)
    error = hist.GetBinError(m_bin)
    h.SetBinContent(bin+1,y)
    h.SetBinError(bin+1,error)
  return h


