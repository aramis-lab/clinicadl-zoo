from typing import Optional

import torch
import torchio as tio


class Template(tio.IntensityTransform):
    """
    Template transform class.


    Parameters
    ----------
    arg1 : float (default 0.0)
        information about arg1.
    arg2 : int (default 1)
        information about arg2.
    """

    def __init__(
        self,
        arg1: float = 0.0,
        arg2: int = 1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.arg1, self.arg2 = arg1, arg2
        self.args_names = ["arg1", "arg2"]

    def apply_transform(self, subject: tio.Subject) -> tio.Subject:
        """ "
        Apply the transform to the subject.
        """
        return subject
