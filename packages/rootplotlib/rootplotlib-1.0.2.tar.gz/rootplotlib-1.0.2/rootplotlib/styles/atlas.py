


__all__ = [ "set_atlas_style",
            "set_atlas_label",
          ]

from ROOT import gROOT, gStyle
from ROOT import TLatex, gPad

import rootplotlib as rpl

def set_atlas_style ():
  
  print ("\nApplying ATLAS style settings...")
  icol=0
  font=42 # Helvetica
  tsize=0.05
  gStyle.SetFrameBorderMode(icol)
  gStyle.SetFrameFillColor(icol)
  gStyle.SetCanvasBorderMode(icol)
  gStyle.SetCanvasColor(icol)
  gStyle.SetPadBorderMode(icol)
  gStyle.SetPadColor(icol)
  gStyle.SetStatColor(icol)
  gStyle.SetPaperSize(20,26)
  gStyle.SetPadTopMargin(0.05)
  gStyle.SetPadRightMargin(0.05)
  gStyle.SetPadBottomMargin(0.16)
  gStyle.SetPadLeftMargin(0.16)
  gStyle.SetTitleXOffset(1.4)
  gStyle.SetTitleYOffset(1.4)
  gStyle.SetTextFont(font)
  gStyle.SetTextSize(tsize)
  gStyle.SetLabelFont(font,"x")
  gStyle.SetTitleFont(font,"x")
  gStyle.SetLabelFont(font,"y")
  gStyle.SetTitleFont(font,"y")
  gStyle.SetLabelFont(font,"z")
  gStyle.SetTitleFont(font,"z")
  gStyle.SetLabelSize(tsize,"x")
  gStyle.SetTitleSize(tsize,"x")
  gStyle.SetLabelSize(tsize,"y")
  gStyle.SetTitleSize(tsize,"y")
  gStyle.SetLabelSize(tsize,"z")
  gStyle.SetTitleSize(tsize,"z")
  gStyle.SetMarkerStyle(20)
  gStyle.SetMarkerSize(1.2)
  gStyle.SetHistLineWidth(2)
  gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes
  gStyle.SetEndErrorSize(0.)
  gStyle.SetOptTitle(0)
  gStyle.SetOptStat(1111)
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(1111)
  gStyle.SetOptFit(0)
  gStyle.SetPadTickX(1)
  gStyle.SetPadTickY(1)
  gStyle.SetPalette(1)


def set_atlas_label( x, y, text, pad=None):

  fig = rpl.get_figure()
  canvas = fig.get_pad(pad)
  canvas.cd()

  experiment = TLatex()
  experiment.SetNDC()
  experiment.SetTextFont(72)
  experiment.SetTextColor(1)
  delx = 0.115*696*gPad.GetWh()/(472*gPad.GetWw())
  experiment.DrawLatex(x,y,'ATLAS')
  label = TLatex()
  label.SetNDC()
  label.SetTextFont(42)
  label.SetTextColor(1)
  label.DrawLatex(x+delx,y,text)

  fig.append(label)
  fig.append(experiment)
  canvas.Modified()
  canvas.Update()



