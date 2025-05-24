#from __future__ import annotations # Allows forward references (e.g., 'Vec3') without NameError at runtime
from typing import Union, List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .Vec3 import Vec3
    from .Quat import Quat

type Vec3Like = Union['Vec3', List[float], Tuple[float, float, float], np.ndarray]
type QuatLike = Union['Quat', List[float], Tuple[float, float, float, float], np.ndarray]