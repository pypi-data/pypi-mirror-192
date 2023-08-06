
import gc
import ROOT

__all__ = ['set_figure', 'get_figure', 'clear', 'suppress_root_warnings']

from . import figures
__all__.extend( figures.__all__ )
from .figures import *

global figure
figure = Figure()

def suppress_root_warnings():
    ROOT.gErrorIgnoreLevel=ROOT.kFatal

def set_figure( canvas ):
    global figure
    figure.set_canvas( canvas )

def get_figure():
    global figure
    return figure

def clear():
    global figure
    figure.clear()

from . import axis
__all__.extend( axis.__all__ )
from .axis import *

from . import canvas
__all__.extend( canvas.__all__ )
from .canvas import *

from . import plots
__all__.extend( plots.__all__ )
from .plots import *

from . import hist1d
__all__.extend( hist1d.__all__ )
from .hist1d import *

from . import hist2d
__all__.extend( hist2d.__all__ )
from .hist2d import *

from . import legends
__all__.extend( legends.__all__ )
from .legends import *

from . import styles
__all__.extend( styles.__all__ )
from .styles import *

from . import colors
__all__.extend( colors.__all__ )
from .colors import *