
# TODO: functionalise, add CLI

import numpy as np
from matplotlib import pyplot
from matplotlib.dates import date2num
from matplotlib.ticker import FuncFormatter, MultipleLocator

from .helpers import DateMappable, ephemeris
from astropy.time import Time


sat_ephem, sat_xyz, sat_ts = ephemeris("oem/A2-2026-04-02.oem")

datemap = DateMappable(sat_ts, 'viridis')
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

cbar = datemap.cbar(ax, now_col="red")

# Points
POINT = dict(marker="o", linestyle='')

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