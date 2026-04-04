
# TODO: functionalise, add CLI

from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from matplotlib import pyplot
from matplotlib.ticker import FuncFormatter, MultipleLocator

from astropy.time import Time

from .helpers import ephemeris
from .date_mappable import DateMappable

OEM_PATH = "oem/A2-2026-04-02.oem"
sat_ephem, sat_xyz, sat_ts = ephemeris(OEM_PATH)

datemap = DateMappable(sat_ts, 'rainbow')
cs = datemap.colors()

# Plot
fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')

# Satellite coord segs

def sat_segments():
    # TODO: move this to `segment` function
    N = len(sat_ts)
    SEGSIZE = 100
    seglims = [
        (i, i + SEGSIZE)
        for i in range(0, N, SEGSIZE)
    ] # HACK: doesn't do entire list?
    return [
        (sat_xyz[a:b].T, cs[a:b])
        for a, b in seglims
    ]

for (xs, ys, zs), cs in sat_segments():
    ax.plot(xs, ys, zs, c=cs[0])

markers = datemap.mark_days()
datemap.mark_now()
cbar = datemap.cbar(ax, now_col="red")

LinearSegmentedColormap

# Points
POINT = dict(marker="o", linestyle='')

for dt, col, size in markers:
    x, y, z = np.array([sat_ephem(Time(dt)).position]).T
    label = None
    if dt.hour == 0:
        label = dt.strftime("  %d")
        ha, va = 'left', 'top'
        if dt.day in (6, 3):
            # HACK: nice positioning
            ha, va = 'right', 'bottom'
        ax.text(
            x[0], y[0], z[0], label,
            ha=ha, va=va, size='xx-small',
            color='black')
    ax.plot(
        x, y, z,
        c=col, markersize=size * 1.5, linestyle='', marker="o")

EARTH = [[0], [0], [0]]
ax.plot(*EARTH, c="green", label="Earth", **POINT)

SAT = np.array([sat_ephem(Time.now()).position]).T
ax.plot(*SAT, c="red", label="Artemis II", **POINT)


ax.legend()
ax.set_title('Earth-centred Inertial / Mm')
ax.set_aspect('equal', 'box')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_major_locator(MultipleLocator(1e5))
    axis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1e3)}"))

pyplot.savefig('artemis2.png')