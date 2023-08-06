

__all__ = [
    'set_lorenzetti_style',
    'set_lorenzetti_label',
]

import rootplotlib as rpl

from ROOT import TLatex, gPad


def set_lorenzetti_style():
    rpl.set_atlas_style ()


def set_lorenzetti_label( x, y, text, pad=None):

  fig = rpl.get_figure()
  canvas = fig.get_pad(pad)
  canvas.cd()
  experiment = TLatex()
  experiment.SetNDC()
  experiment.SetTextFont(72)
  experiment.SetTextColor(1)
  delx = 0.17*696*gPad.GetWh()/(472*gPad.GetWw())
  experiment.DrawLatex(x,y,'Lorenzetti')
  label = TLatex()
  label.SetNDC()
  label.SetTextFont(42)
  label.SetTextColor(1)
  label.DrawLatex(x+delx,y,text)
  fig.append(label)
  fig.append(experiment)
  canvas.Modified()
  canvas.Update()
