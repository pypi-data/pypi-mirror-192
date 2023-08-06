

__all__ = ['get_color']

from ROOT import TColor


def get_color(color, transparency = None):
    try:
      color = TColor.GetColor( *color )
    except:
      if type(color) is not int: color = TColor.GetColor( color )
    if transparency is not None:
      color = TColor.GetColorTransparent( color, transparency )
    return color
