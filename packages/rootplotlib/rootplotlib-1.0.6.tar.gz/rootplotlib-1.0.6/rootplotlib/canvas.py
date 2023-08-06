
__all__ = ['format_canvas_axes', 'create_canvas', 'create_ratio_canvas', 'format_ratio_canvas_axes']

from ROOT import TCanvas, TPad
import rootplotlib as rpl


def create_canvas( name, title='', canw=700, canh=500 ):
    canvas = TCanvas( name, title, canw, canh )
    fig = rpl.get_figure()
    fig.set_canvas(canvas)
    return fig



def create_ratio_canvas( name, title='', canw=500, canh=600, ratio_size_as_fraction=0.35, drawopt='pE1'):

    canvas = TCanvas(name,title,canw,canh)
    fig = rpl.get_figure()
    fig.set_canvas(canvas)
    canvas.SetFillStyle(4050)

    # Top
    canvas.cd()
    top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
    top.SetBottomMargin(0.02/float(top.GetHNDC()))
    top.SetTopMargin   (0.04/float(top.GetHNDC()))
    top.SetRightMargin (0.05 )
    top.SetLeftMargin  (0.16 )
    top.SetFillColor(0)
    top.Draw(drawopt)
    fig.append(top)

    # Bot
    canvas.cd()
    bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
    bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
    bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
    bot.SetRightMargin (0.05)
    bot.SetLeftMargin  (0.16)
    bot.SetFillColor(0)
    bot.Draw(drawopt)
    fig.append(bot)

    return fig



def format_canvas_axes(  XTitleSize   = 22
                        ,XTitleOffset = 0.98
                        ,XTitleFont   = 43
                        ,XLabelSize   = 22
                        ,XLabelOffset = 0.002
                        ,XLabelFont   = 43
                        ,XNDiv = None

                        ,YTitleSize   = 22
                        ,YTitleOffset = 1.75
                        ,YTitleFont   = 43
                        ,YLabelSize   = 22
                        ,YLabelOffset = 0.006
                        ,YLabelFont   = 43
                        ,YNDiv = [10,5,0]

                        ,ZTitleSize   = 22
                        ,ZTitleOffset = 0.85
                        ,ZTitleFont   = 43
                        ,ZLabelSize   = 22
                        ,ZLabelOffset = 0.002
                        ,ZLabelFont   = 43
                        ,pad = None
                        ) :

    fig = rpl.get_figure()
    canvas = fig.get_pad(pad)

    for primitive in canvas.GetListOfPrimitives() :
        if not hasattr(primitive,'GetXaxis') :
            continue
        primitive.GetXaxis().SetTitleSize  (XTitleSize  )
        primitive.GetXaxis().SetTitleOffset(XTitleOffset/float(canvas.GetHNDC()))
        primitive.GetXaxis().SetTitleFont  (XTitleFont  )
        primitive.GetXaxis().SetLabelSize  (XLabelSize  )
        primitive.GetXaxis().SetLabelOffset(XLabelOffset/float(canvas.GetHNDC()))
        primitive.GetXaxis().SetLabelFont  (XLabelFont  )
        primitive.GetXaxis().SetTickLength(0.02/float(canvas.GetHNDC()))
        if XNDiv:
            primitive.GetXaxis().SetNdivisions (XNDiv[0],XNDiv[1],XNDiv[2])
        primitive.GetYaxis().SetTitleSize  (YTitleSize  )
        primitive.GetYaxis().SetTitleOffset(YTitleOffset)
        primitive.GetYaxis().SetTitleFont  (YTitleFont  )
        primitive.GetYaxis().SetLabelSize  (YLabelSize  )
        primitive.GetYaxis().SetLabelOffset(YLabelOffset)
        primitive.GetYaxis().SetLabelFont  (YLabelFont  )
        primitive.GetYaxis().SetNdivisions (YNDiv[0],YNDiv[1],YNDiv[2])
        if not hasattr(primitive,'GetZaxis') :
            continue
        primitive.GetZaxis().SetTitleSize  (ZTitleSize  )
        primitive.GetZaxis().SetTitleOffset(ZTitleOffset)
        primitive.GetZaxis().SetTitleFont  (ZTitleFont  )
        primitive.GetZaxis().SetLabelSize  (ZLabelSize  )
        primitive.GetZaxis().SetLabelOffset(ZLabelOffset)
        primitive.GetZaxis().SetLabelFont  (ZLabelFont  )
        # if here, we setup x, y and z axis
        break
    canvas.Modified()
    canvas.Update()




def format_ratio_canvas_axes(  XTitleSize   = 22
                              ,XTitleOffset = 0.98
                              ,XTitleFont   = 43
                              ,XLabelSize   = 22
                              ,XLabelOffset = 0.002
                              ,XLabelFont   = 43
      
                              ,YTitleSize   = 22
                              ,YTitleOffset = 1.75
                              ,YTitleFont   = 43
                              ,YLabelSize   = 22
                              ,YLabelOffset = 0.006
                              ,YLabelFont   = 43
                              ,YNDiv = [10,5,0]
      
                              ,ZTitleSize   = 22
                              ,ZTitleOffset = 0.85
                              ,ZTitleFont   = 43
                              ,ZLabelSize   = 22
                              ,ZLabelOffset = 0.002
                              ,ZLabelFont   = 43
                              ) :

   
    format_canvas_axes(pad='pad_top',XLabelOffset=0.1
                     ,XTitleSize=XTitleSize,XTitleOffset=XTitleOffset,XTitleFont=XTitleFont
                     ,XLabelSize=XLabelSize,XLabelFont=XLabelFont
                     ,YTitleSize=YTitleSize,YTitleOffset=YTitleOffset,YTitleFont=YTitleFont
                     ,YLabelSize=YLabelSize,YLabelOffset=YLabelOffset,YLabelFont=YLabelFont
                     ,YNDiv=YNDiv
                     ,ZTitleSize=ZTitleSize,ZTitleOffset=ZTitleOffset,ZTitleFont=ZTitleFont
                     ,ZLabelSize=ZLabelSize,ZLabelOffset=ZLabelOffset,ZLabelFont=ZLabelFont
                      )
    format_canvas_axes(pad='pad_bot',YLabelOffset=0.009
                     ,XTitleSize=XTitleSize,XTitleOffset=XTitleOffset,XTitleFont=XTitleFont
                     ,XLabelSize=XLabelSize,XLabelOffset=XLabelOffset,XLabelFont=XLabelFont
                     ,YTitleSize=YTitleSize,YTitleOffset=YTitleOffset,YTitleFont=YTitleFont
                     ,YLabelSize=YLabelSize,YLabelFont=YLabelFont
                     ,YNDiv = [5,5,0]
                     ,ZTitleSize=ZTitleSize,ZTitleOffset=ZTitleOffset,ZTitleFont=ZTitleFont
                     ,ZLabelSize=ZLabelSize,ZLabelOffset=ZLabelOffset,ZLabelFont=ZLabelFont
                     )


def savefig( output ):
    fig = rpl.get_figure()
    fig.savefig(output)