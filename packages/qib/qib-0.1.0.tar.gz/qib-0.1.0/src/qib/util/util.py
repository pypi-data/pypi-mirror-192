import numpy as np
from typing import Sequence
from qib.field import Field, Particle


def crandn(size):
    """
    Draw random samples from the standard complex normal (Gaussian) distribution.
    """
    # 1/sqrt(2) is a normalization factor
    return (np.random.standard_normal(size)
       + 1j*np.random.standard_normal(size)) / np.sqrt(2)


def permute_gate_wires(u: np.ndarray, perm):
    """
    Transpose (permute) the wires of a quantum gate stored as NumPy array.
    """
    nwires = len(perm)
    assert u.shape == (2**nwires, 2**nwires)
    perm = list(perm)
    u = np.reshape(u, (2*nwires) * (2,))
    u = np.transpose(u, perm + [nwires + p for p in perm])
    u = np.reshape(u, (2**nwires, 2**nwires))
    return u


def map_particle_to_wire(fields: Sequence[Field], p: Particle):
    """
    Map a particle to a quantum wire.
    """
    i = 0
    for f in fields:
        if p.field == f:
            i += p.index
            return i
        else:
            i += f.lattice.nsites
    # not found
    return -1
