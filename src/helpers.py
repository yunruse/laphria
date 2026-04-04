import numpy as np

from oem import OrbitEphemerisMessage

def ephemeris(path: str):
    ephem = OrbitEphemerisMessage.open(path)
    xyz = np.array([state.position for state in ephem.states])
    ts = np.array([state.epoch.datetime64 for state in ephem.states])

    # TODO: transform coordinates; think about input space
    # and ensure Ephem works nicely therein?
    # probably transform the ephem itself..?

    return ephem, xyz, ts

def segments[T](*iterable: list[T], segsize=100):
    pass
    # TODO: some kind of iterable approach???
