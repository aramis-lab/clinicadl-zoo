from typing import Union

from clinicadl.utils.config import DefaultFromLibrary

from .base import ZooTransformConfig


class TemplateConfig(ZooTransformConfig):
    """
    Config class for :py:class:`clinicadl_zoo.transforms.Template`.
    """

    arg1: float
    arg2: int

    def __init__(
        self,
        arg1: float,
        arg2: Union[int, DefaultFromLibrary] = DefaultFromLibrary.YES,
    ):
        super().__init__(arg1=arg1, arg2=arg2)
