
__all__ = [ 'set_xlabel',
            'set_ylabel',
            'set_axis_labels',
            'fix_xaxis_ranges',
            'fix_yaxis_ranges',
            'set_yaxis_ranges',
            'get_yaxis_ranges',
           ]

import rootplotlib as rpl


def set_xlabel(xlabel, pad=None):
    fig = rpl.get_figure()
    fig.set_xlabel( xlabel, pad=pad )


def set_ylabel(ylabel, pad=None):
    fig = rpl.get_figure()
    fig.set_ylabel( ylabel, pad=pad )


def set_axis_labels(xlabel, ylabel,yratiolabel='ratio'):

    fig = rpl.get_figure()
    if fig.get_pad('pad_top'):
        set_ylabel( ylabel, pad='pad_top')
        set_ylabel( yratiolabel, pad='pad_bot')
        set_xlabel( xlabel, pad='pad_bot')
    else:
        set_xlabel( xlabel )
        set_ylabel( ylabel )


def fix_xaxis_ranges(xminf=1., xminc=0., xmaxf=1., xmaxc=0., only_filled=False, pad=None):
    fig = rpl.get_figure()
    xmin, xmax = fig.get_xaxis_ranges( only_filled = only_filled , pad=pad)
    fig.set_xaxis_ranges(xmin*xminf+xminc, xmax*xmaxf+xmaxc, for_all=True, pad=pad)



def fix_yaxis_ranges(yminf=1., yminc=0., ymaxf=1., ymaxc=0., ignore_zeros=True, ignore_errors=False, pad=None):
    fig = rpl.get_figure()
    ymin, ymax = fig.get_yaxis_ranges(pad=pad, ignore_zeros=ignore_zeros, ignore_errors=ignore_errors)
    fig.set_yaxis_ranges(ymin*yminf+yminc, ymax*ymaxf+ymaxc, pad=pad)


def set_yaxis_ranges( ymin , ymax, pad=None ):
    fig = rpl.get_figure()
    fig.set_yaxis_ranges(ymin, ymax, pad=pad)


def get_yaxis_ranges( pad=None ):
    fig = rpl.get_figure()
    return fig.get_yaxis_ranges(pad=pad, ignore_zeros=False, ignore_errors=False)
