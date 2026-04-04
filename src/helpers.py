import numpy as np

from numpy.typing import NDArray

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
    time: NDArray[np.datetime64]
    scalar: NDArray[np.float64]

    cmap: Colormap
    norm: Normalize
    mappable: ScalarMappable

    markers: list[np.datetime64]
    marker_cols: list[str]
    marker_widths: list[float]

    def __init__(
        self,
        time_series: NDArray[np.datetime64],
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

        self.markers = []
        self.marker_cols = []
        self.marker_widths = []

    def mark_now(self, now_col: str = "red"):
        self.markers.append(Time.now().datetime64)
        self.marker_cols.append(now_col)
        self.marker_widths.append(2.5)

    def mark_days(self):
        "Add date markers."
        # TODO: thickish black every midnight (UTC)...
        #       thin white at 6am and 6pm...
        #       thin black at noon

        # TODO: return the above as points
        # for showing on the plot as well!

    def colors(self):
        return self.mappable.to_rgba(self.scalar)

    def cbar(
        self,
        ax: Axes,
        now_col: str | None = None,
    ):
        # TODO: segmentation of cbar?
        cbar = pyplot.colorbar(self.mappable, ax=ax)
        loc = AutoDateLocator()
        cbar.ax.yaxis.set_major_locator(loc)
        cbar.ax.yaxis.set_major_formatter(ConciseDateFormatter(loc))

        # TODO: add other 'markers'

        if self.markers:
            cbar.add_lines(
                date2num(self.markers),
                self.marker_cols,
                self.marker_widths
            )

        return cbar

def segments[T](*iterable: list[T], segsize=100):
    pass
    # TODO: some kind of iterable approach???
