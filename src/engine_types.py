"""
User defined datastructures and types used across the engine
"""

from typing import Sequence, TypeAlias, Self, Iterator
from dataclasses import dataclass, fields
from enum import Enum
from abc import ABC

@dataclass(frozen=True, slots=True)
class _VecBase(ABC):
    """ 
    Baseclass for 2 & 3 dimensional data stored in dataclasses 

    Implements:
        __iter__
        __len__
        __add__
        __sub__
        __mul__
        __imul__
    """
    def _values(self) -> tuple[float, ...]:
        return tuple(getattr(self, f.name) for f in fields(self))
    
    def __iter__(self) -> Iterator[float]:
        for f in fields(self):
            yield getattr(self, f.name)

    def __len__(self) -> int:
        return len(tuple(self))

    def __add__(self, other: Self) -> Self:
        if type(self) is not type(other):
            return NotImplemented
        return type(self)(*(a + b for a, b in zip(self._values(), other._values())))
    
    def __sub__(self, other: Self) -> Self:
        if type(self) is not type(other):
            return NotImplemented
        return type(self)(*(a - b for a, b in zip(self._values(), other._values())))

    def __mul__(self, scalar: float) -> Self:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return type(self)(*(a * scalar for a in self._values()))

    def __rmul__(self, scalar: float) -> Self:
        return self * scalar

@dataclass(frozen=True, slots=True)
class Vector3(_VecBase):
    """ Represents vectorial 3D data """
    x: float
    y: float
    z: float

@dataclass(frozen=True, slots=True)
class Vector2(_VecBase):
    """ Represents vectorial 2D data """
    x: float
    y: float

@dataclass(frozen=True, slots=True)
class Coordinate3(_VecBase):
    """ Represents scalar 3D data """
    x: float
    y: float
    z: float

@dataclass(frozen=True, slots=True)
class Coordinate2(_VecBase):
    """ Represents scalar 2D data """
    x: float
    y: float

@dataclass(frozen=True, slots=True)
class Color:
    """ Represents RGBA color """
    r: int
    g: int
    b: int
    a: int

Edge3: TypeAlias = Sequence[Coordinate3] # Represents a 3D object's edge
Face3: TypeAlias = Sequence[Coordinate3] # Represents a 3D object's face

class MeshType(Enum):
    CUBE = "CUBE"
    PYRAMID = "PYRAMID"
    OCTAHEDRON = "OCTAHEDRON"