from typing import Optional, Union

from clinicadl.utils.config import DefaultFromLibrary

from .base import ZooTransformConfig


class NanRemovalConfig(ZooTransformConfig):
    """
    Config class for :py:class:`clinicadl_zoo.transforms.NanRemoval`.
    """

    nan: float
    posinf: Optional[float]
    neginf: Optional[float]

    def __init__(
        self,
        nan: Union[float, DefaultFromLibrary] = DefaultFromLibrary.YES,
        posinf: Union[Optional[float], DefaultFromLibrary] = DefaultFromLibrary.YES,
        neginf: Union[Optional[float], DefaultFromLibrary] = DefaultFromLibrary.YES,
    ):
        super().__init__(nan=nan, posinf=posinf, neginf=neginf)
