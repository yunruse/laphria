from dataclasses import dataclass, field
from datetime import datetime

import numpy as np
from numpy.typing import NDArray

from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num
from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Colormap, Normalize

from astropy.time import Time

from .dt_helpers import dt64_to_dt, dt_to_dt64, marks_between

@dataclass
class DateMarkers:
    datetimes: list[datetime] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    sizes: list[float] = field(default_factory=list)

    def __iter__(self):
        return zip(self.datetimes, self.colors, self.sizes)

class DateMappable:
    time: NDArray[np.datetime64]
    scalar: NDArray[np.float64]
    start: datetime
    end: datetime

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
        self.start = dt64_to_dt(time_series[0])
        self.end = dt64_to_dt(time_series[-1])
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
        "Add date markers, and return properties used"

        markers = DateMarkers()

        for date in marks_between(self.start, self.end, hours=6):
            match date.hour:
                case 0:
                    col = "black"
                    size = 2
                case 12:
                    col = "black"
                    size = 1
                case 6 | 18:
                    col = "white"
                    size = 0.5
                case _:
                    raise ValueError(f"{date} has hour {date.hour} not at 6hr offset!")

            markers.datetimes.append(date)
            markers.colors.append(col)
            markers.sizes.append(size)

        self.markers += [dt_to_dt64(dt) for dt in markers.datetimes]
        self.marker_cols += markers.colors
        self.marker_widths += markers.sizes

        return markers

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
        fmts = [''] * 6
        fmts[2] = "%a %d"
        cbar.ax.yaxis.set_major_formatter(ConciseDateFormatter(loc, formats=fmts))

        # TODO: add other 'markers'

        if self.markers:
            cbar.add_lines(
                date2num(self.markers),
                self.marker_cols,
                self.marker_widths
            )

        return cbar