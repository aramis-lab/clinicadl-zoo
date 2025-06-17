from pathlib import Path
from typing import Optional, Union

from clinicadl.utils.config import DefaultFromLibrary

from .base import ZooTransformConfig


class HypometabolismConfig(ZooTransformConfig):
    """
    Config class for :py:class:`clinicadl_zoo.transforms.Hypometabolism`.
    """

    mask_dir: Union[str, Path]
    pathology: str
    percentage: int
    sigma: Union[int, DefaultFromLibrary] = DefaultFromLibrary.YES

    def __init__(
        self,
        mask_dir: Union[str, Path],
        pathology: str,
        percentage: int,
        sigma: Optional[int] = 2,
    ):
        super().__init__(
            mask_dir=mask_dir, pathology=pathology, percentage=percentage, sigma=sigma
        )
