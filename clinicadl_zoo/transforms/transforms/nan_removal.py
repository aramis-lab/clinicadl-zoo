from typing import Optional, get_type_hints

import torch
import torchio as tio
from clinicadl.data.structures import DataPoint


class NanRemoval(tio.Transform):
    """
    Replaces NaN, positive infinity, and negative infinity values.

    See also :py:func:`torch.nan_to_num`.

    Parameters
    ----------
    nan : float (optional, default=0.0)
        the value to replace NaN with.
    posinf : Optional[float] (optional, default=None)
        the value to replace positive infinity values with. If None,
        positive infinity values are replaced with the greatest finite
        value representable by image’s dtype.
    neginf : Optional[float] (optional, default=None)
        the value to replace negative infinity values with. If None,
        negative infinity values are replaced with the lowest finite
        value representable by image’s dtype.
    """

    def __init__(
        self,
        nan: float = 0.0,
        posinf: Optional[float] = None,
        neginf: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.nan, self.posinf, self.neginf = nan, posinf, neginf
        self.args_names = ["nan", "posinf", "neginf"]

    def apply_transform(self, datapoint: DataPoint) -> DataPoint:
        for image in datapoint.get_images(intensity_only=True):
            image.set_data(self._nan_removal(image.tensor))
        return datapoint

    def _nan_removal(self, tensor: torch.Tensor) -> torch.Tensor:
        return tensor.nan_to_num(self.nan, self.posinf, self.neginf)
