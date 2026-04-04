from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter

from oem import OrbitEphemerisMessage

import numpy as np


def ephemeris(path: str):
    ephem = OrbitEphemerisMessage.open(path)
    xyz = np.array([state.position for state in ephem.states])
    ts = np.array([state.epoch.datetime64 for state in ephem.states])

    # TODO: transform coordinates; think about input space
    # and ensure Ephem works nicely therein?
    # probably transform the ephem itself..?

    return ephem, xyz, ts

def segmented_map(ss, cmap='viridis'):
    cmap = pyplot.colormaps[cmap]

    norm = Normalize(vmin=ss[0], vmax=ss[-1])
    mappable = ScalarMappable(norm=norm, cmap=cmap)
    # TODO: segmentation!
    return mappable

def date_cbar(ax: Axes, mappable: ScalarMappable):
    cbar = pyplot.colorbar(mappable, ax=ax)
    loc = AutoDateLocator()
    cbar.ax.yaxis.set_major_locator(loc)
    cbar.ax.yaxis.set_major_formatter(ConciseDateFormatter(loc))
    return cbar

def segments[T](*iterable: list[T], segsize=100):
    pass
    # TODO: some kind of iterable approach???
