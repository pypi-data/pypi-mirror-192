
__all__ = ['add_text', 'add_legend']

from ROOT import TLegend, TLatex, TH1, TH2
import rootplotlib as rpl


def add_text(x,y,text,color=1, textfont=42, textsize=0.1, pad=None):
    fig = rpl.get_figure()
    pad = fig.get_pad(pad)
    pad.cd()
    tex = TLatex()
    tex.SetNDC()
    tex.SetTextFont(textfont)
    tex.SetTextColor(color)
    tex.SetTextSize(textsize)
    tex.DrawLatex(x,y,text)
    fig.add_legend(tex)


def add_legend( legends, x1=.8, y1=.8, x2=.9, y2=.9, pad=None, textsize=18, ncolumns=1, option='f', squarebox=True, title=''):

    fig = rpl.get_figure()
    canvas = fig.get_pad(pad)
    leg = TLegend(x1,y1,x2,y2,title)
    leg.SetName('legend' + ("_" + title if title else ""))
    leg.SetTextFont(43)
    leg.SetTextSize(textsize)
    leg.SetTextFont(43)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(ncolumns)

    primitives = []
    for primitive in canvas.GetListOfPrimitives():
        if issubclass(type(primitive), TH1) or issubclass(type(primitive),TH2):
            primitives.append( primitive )

    for idx, legend in enumerate(legends): 
        leg.AddEntry(primitives[idx], legend, option) # plef

    # recipe for making roughly square boxes
    if squarebox:
        h = leg.GetY2()-leg.GetY1()
        w = leg.GetX2()-leg.GetX1()
        if leg.GetNRows():
            leg.SetMargin(leg.GetNColumns()*h/float(leg.GetNRows()*w))
    leg.SetHeader("#font[63]{" + title + "}")
    fig.add_legend(leg)
 
