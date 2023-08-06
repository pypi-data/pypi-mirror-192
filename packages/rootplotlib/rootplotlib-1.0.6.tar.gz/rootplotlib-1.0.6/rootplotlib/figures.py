
__all__ = ['Figure']


from ROOT import TH1, TH2
import itertools
import gc
import sys

class Figure( object ):

    def __init__(self, canvas=None):
        self.__canvas = canvas
        self.__collections = []


    def canvas(self):
        return self.__canvas


    def set_canvas( self , canvas ):
        self.__canvas = canvas
        self.__collections = []


    def clear(self):
        self.__canvas.Close()
        for obj in self.__collections:
            if obj:
                obj.Delete()
        self.__collections = []
        gc.collect()


    def append(self, obj):
        self.__collections.append(obj)


    #
    # Get pad. If none or not exist, return the main canvas
    #
    def get_pad( self, pad=None ):

        if pad and (pad==primitive.GetName() for primitive in self.__canvas.GetListOfPrimitives()):
            canvas = self.__canvas.GetPrimitive(pad)
        else:
            canvas = self.__canvas  
        return canvas


    #
    # Add histogram into the figure
    #
    def add_hist(self, hist,  drawopt='pE1', pad=None):
        canvas = self.get_pad(pad)
        if not "same" in drawopt: drawopt += ' sames'
        canvas.cd()
        hist.Draw(drawopt) # add into the list of primitives
        canvas.Modified()
        canvas.Update()
        self.append(hist)

    #
    # Add legend into the figure
    #
    def add_legend(self, leg, pad=None):
        canvas = self.get_pad(pad)
        canvas.cd()
        leg.Draw() # add into the list of primitives
        canvas.Modified()
        canvas.Update()
        self.append(leg)

    #
    # Set x label
    #
    def set_xlabel(self, xlabel, pad=None):

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives() :
            if hasattr(primitive,'GetXaxis') :
                primitive.GetXaxis().SetTitle(xlabel)
                break
        canvas.Modified()
        canvas.Update()


    #
    # Set y label
    #
    def set_ylabel(self, ylabel, pad=None):

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives() :
            if hasattr(primitive,'GetYaxis') :
                primitive.GetYaxis().SetTitle(ylabel)
                break
        canvas.Modified()
        canvas.Update()


    def get_xaxis(self, pad=None):

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives():
            if issubclass(type(primitive),TH1):
                return primitive.GetXaxis()
            elif issubclass(type(primitive),TH2):
                return primitive.GetXaxis()

        return None

    def get_yaxis(self, pad=None):

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives():
            if issubclass(type(primitive),TH1):
                return primitive.GetYaxis()
            elif issubclass(type(primitive),TH2):
                return primitive.GetXaxis()
        return None


    #
    # Get xmin and xmax values into the canvas
    #
    def get_xaxis_ranges(self, only_filled=False, pad=None):
    
        xmin = sys.float_info.max
        xmax = sys.float_info.min
        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives():
            if issubclass(type(primitive),TH1):
                axis = primitive.GetXaxis()
                if only_filled:
                    bins = [primitive.GetBinCenter(idx) for idx in range(1,primitive.GetNbinsX()+1) if primitive.GetBinContent(idx)>0]
                    if len(bins)>=2:
                        xmin = min(xmin,bins[0])
                        xmax = max(xmax,bins[-1])
                else:
                    xmin = min(xmin,axis.GetXmin())
                    xmax = max(xmax,axis.GetXmax())
        return xmin, xmax



    def set_xaxis_ranges(self, xmin, xmax, for_all=False, pad=None):

        # Get the axis from canvas
        axis = self.get_xaxis(pad)
        canvas = self.get_pad(pad)
        if not axis:
            print ('Warning: set_x_axis_ranges had no effect. Check that your canvas has plots in it.')
        else:
            if for_all: 
                axis.SetRangeUser(xmin,xmax)
            else: 
                axis.SetLimits(xmin,xmax)
            canvas.Modified()
            canvas.Update()


    def get_yaxis_ranges(self, pad=None, ignore_zeros=False, ignore_errors=False):

        ymin = sys.float_info.max
        ymax = sys.float_info.min
        canvas = self.get_pad(pad)

        for primitive in canvas.GetListOfPrimitives():

            if isinstance(primitive, TH2):
                x = primitive.GetXaxis()
                y = primitive.GetYaxis()
                nx = primitive.GetNbinsY()
                ny = primitive.GetNbinsY()
                # This is just a workaround for candles/violins
                for rxc, ryc in itertools.product( range(1,nx+1), range(1,ny+1)):
                    z = primitive.GetBinContent(rxc,ryc)
                    if ignore_zeros and z == 0 :
                        continue
                    ymin = min(ymin,y.GetBinCenter(ryc))
                    ymax = max(ymax,y.GetBinCenter(ryc))
                return ymin, ymax

            elif issubclass(type(primitive),TH1) :
                ysum = 0
                for bin in range(primitive.GetNbinsX()) :
                    ysum = ysum+primitive.GetBinContent(bin+1)
                if ysum == 0: ignore_zeros = 0
                for bin in range(primitive.GetNbinsX()) :
                    y = primitive.GetBinContent(bin+1)
                    if ignore_errors :
                        ye = 0
                    else :
                        ye = primitive.GetBinError(bin+1)
                    if ignore_zeros and y == 0 :
                        continue
                    ymin = min(ymin,y-ye)
                    ymax = max(ymax,y+ye)

        return ymin, ymax


    def set_yaxis_ranges(self, ymin, ymax, pad=None):

        axis = self.get_yaxis(pad)
        canvas = self.get_pad(pad)
        if not axis :
            print ('Warning: SetYaxisRange had no effect. Check that your canvas has plots in it.')
        else:
            axis.SetRangeUser(ymin,ymax)
            canvas.Modified()
            canvas.Update()


    def savefig(self, output):
        self.__canvas.SaveAs(output)


    def show(self):
        self.__canvas.Draw()
