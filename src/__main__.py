
# TODO: functionalise, add CLI
from astropy.time import Time

import numpy as np
from matplotlib import pyplot
from matplotlib.dates import date2num
from matplotlib.ticker import FuncFormatter, MultipleLocator

from .helpers import date_cbar, ephemeris, segmented_map, segments


sat_ephem, sat_xyz, sat_ts = ephemeris("oem/A2-2026-04-02.oem")
ss = date2num(sat_ts)

mappable = segmented_map(ss, 'viridis')
cs = mappable.to_rgba(ss)

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

cbar = date_cbar(ax, mappable)
dnow: float = date2num(Time.now().datetime64)
cbar.add_lines([dnow], colors=["red"], linewidths=[2.5])

# ax.plot(*sat_xyz.T, linestyle='-', label="Sat")

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