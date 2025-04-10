from typing import Optional, Union

import torchio as tio
from clinicadl.transforms.config import TransformConfig
from clinicadl.utils.config import DefaultFromLibrary
from pydantic import computed_field

from ..enum import ZooTransform
from ..transforms.nan_removal import NanRemoval


class NanRemovalConfig(TransformConfig):
    """
    Config class for :py:class:`~clinicadl_zoo.transforms.transforms.NanRemoval`.
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

    @computed_field
    @property
    def name(self) -> str:
        """The name of the transform."""
        return ZooTransform.NAN_REMOVAL.value

    def _get_class(self) -> type[tio.Transform]:
        """Returns the transform associated to this config class."""
        return NanRemoval
