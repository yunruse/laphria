import numpy as np

from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num
from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Colormap, Normalize

from oem import OrbitEphemerisMessage
from astropy.time import Time

def ephemeris(path: str):
    ephem = OrbitEphemerisMessage.open(path)
    xyz = np.array([state.position for state in ephem.states])
    ts = np.array([state.epoch.datetime64 for state in ephem.states])

    # TODO: transform coordinates; think about input space
    # and ensure Ephem works nicely therein?
    # probably transform the ephem itself..?

    return ephem, xyz, ts

class DateMappable:
    time: np.ndarray  # TODO: typing better?
    scalar: np.ndarray

    cmap: Colormap
    norm: Normalize
    mappable: ScalarMappable

    def __init__(
        self,
        time_series,
        cmap: str | Colormap = 'viridis',

    ):

        if isinstance(cmap, str):
            self.cmap = pyplot.colormaps[cmap]
        else:
            self.cmap = cmap

        self.time = time_series
        self.scalar = date2num(self.time)

        self.norm = Normalize(vmin=self.scalar[0], vmax=self.scalar[-1])
        self.mappable = ScalarMappable(norm=self.norm, cmap=self.cmap)

        # TODO: segmentation!
    
    def colors(self):
        return self.mappable.to_rgba(self.scalar)

    def cbar(
        self,
        ax: Axes,
        now_col: str | None = None,
    ):
        cbar = pyplot.colorbar(self.mappable, ax=ax)
        loc = AutoDateLocator()
        cbar.ax.yaxis.set_major_locator(loc)
        cbar.ax.yaxis.set_major_formatter(ConciseDateFormatter(loc))

        # TODO: add other 'markers'

        if now_col:
            dnow: float = date2num(Time.now().datetime64)
            cbar.add_lines([dnow], colors=[now_col], linewidths=[2.5])

        return cbar

def segments[T](*iterable: list[T], segsize=100):
    pass
    # TODO: some kind of iterable approach???
