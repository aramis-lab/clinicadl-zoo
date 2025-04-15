import torchio as tio
from clinicadl.data.structures import DataPoint


class Template(tio.IntensityTransform):
    """
    Template transform class.

    Parameters
    ----------
    arg1 : float
        Description of arg1.
    arg2 : int (default=0)
        Description of arg2.
    """

    def __init__(
        self,
        arg1: float,
        arg2: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.arg1, self.arg2 = arg1, arg2
        self.args_names = ["arg1", "arg2"]

    def apply_transform(self, datapoint: DataPoint) -> DataPoint:   # pylint: disable=arguments-renamed
        """
        Apply the transform to the datapoint.
        """
        return datapoint
