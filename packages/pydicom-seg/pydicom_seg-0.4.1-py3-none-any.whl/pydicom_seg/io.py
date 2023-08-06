from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class ImageDescription:
    origin: Tuple[float, ...]
    direction: np.ndarray
    spacing: Tuple[float, ...]
    data: np.ndarray


from types import FunctionType
from functools import wraps
def requires_module(
    name: str
):
    def _decorator(obj):
        is_func = isinstance(obj, FunctionType)
        call_obj = obj if is_func else obj.__init__
        available = True
        try:
            __import__(name)
        except ImportError:
            available = False

        @wraps(call_obj)
        def _wrapper(*args, **kwargs):
            if not available:
                err_msg = f"Required module `{name}` is not installed."
                raise ImportError(err_msg)

            return call_obj(*args, **kwargs)

        if is_func:
            return _wrapper
        obj.__init__ = _wrapper
        return obj

    return _decorator


@requires_module("itk")
def to_itk(desc: ImageDescription) -> "itk.Image":
    import itk
    image = itk.GetImageFromArray(desc.data)
    image.SetOrigin(desc.origin)
    image.SetDirection(desc.direction)
    image.SetSpacing(desc.spacing)
    return image


@requires_module("SimpleITK")
def to_simpleitk(desc: ImageDescription) -> "SimpleITK.Image":
    import SimpleITK as sitk
    image = sitk.GetImageFromArray(desc.data)
    image.SetOrigin(desc.origin)
    image.SetDirection(desc.direction)
    image.SetSpacing(desc.spacing)
    return image
