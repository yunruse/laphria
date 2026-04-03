
from oem import OrbitEphemerisMessage
from astropy.time import Time

import numpy as np
from matplotlib import pyplot
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MultipleLocator


sat_ephem = OrbitEphemerisMessage.open("oem/A2-2026-04-02.oem")
sat_xyz = np.array([state.position for state in sat_ephem.states])

# time and cmap thereof
ts = np.array([state.epoch.datetime64 for state in sat_ephem.states])
ss = mdates.date2num(ts)

cmap = pyplot.colormaps['viridis']

norm = Normalize(vmin=ss[0], vmax=ss[-1])
mappable = ScalarMappable(norm=norm, cmap=cmap)
cs = mappable.to_rgba(ss)

# Plot
fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')

# Satellite coord segs
N = len(ts)
SEGSIZE = 100
seglims = [
    (i, i + SEGSIZE)
    for i in range(0, N, SEGSIZE)
] # HACK: doesn't do entire list?

segments = [
    (sat_xyz[a:b].T, cs[a:b])
    for a, b in seglims
]

for (xs, ys, zs), cs in segments:
    ax.plot(xs, ys, zs, c=cs[0])

cbar = pyplot.colorbar(mappable, ax=ax)

loc = mdates.AutoDateLocator()
cbar.ax.yaxis.set_major_locator(loc)
cbar.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

dnow: float = mdates.date2num(Time.now().datetime64)
cbar.add_lines([dnow], colors=["red"], linewidths=[2.5])


# ax.plot(*sat_xyz.T, linestyle='-', label="Sat")

ax.set_aspect('equal', 'box')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_major_locator(MultipleLocator(1e5))
    axis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1e3)}"))

# Points

ax.plot([0], [0], [0], marker="o", c="green", linestyle='', label="Earth")

xyz = np.array([sat_ephem(Time.now()).position])
ax.plot(*xyz.T, marker="o", linestyle='', c="red", label="Artemis II")

ax.set_title('Earth-centred Inertial / Mm')
ax.legend()
pyplot.savefig('artemis2.png')