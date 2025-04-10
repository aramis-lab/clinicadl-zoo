from typing import Union

import torchio as tio
from clinicadl.transforms.config import TransformConfig
from clinicadl.utils.config import DefaultFromLibrary
from pydantic import computed_field

from ..enum import ZooTransform
from ..transforms.template import Template


class TemplateConfig(TransformConfig):
    """
    Config class for :py:class:`~clinicadl_zoo.transforms.transforms.Template`.
    """

    arg1: float
    arg2: int

    def __init__(
        self,
        arg1: Union[float, DefaultFromLibrary] = DefaultFromLibrary.YES,
        arg2: Union[int, DefaultFromLibrary] = DefaultFromLibrary.YES,
    ):
        super().__init__(arg1=arg1, arg2=arg2)

    @computed_field
    @property
    def name(self) -> str:
        """The name of the transform."""
        return ZooTransform.TEMPLATE.value

    def _get_class(self) -> type[tio.Transform]:
        """Returns the transform associated to this config class."""
        return Template
