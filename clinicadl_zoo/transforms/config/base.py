import torchio as tio
from clinicadl.transforms.config import TransformConfig

import clinicadl_zoo.transforms as zoo_transforms


class ZooTransformConfig(TransformConfig):
    """
    Base config class for transforms in ClinicaDL Transform Zoo.
    """

    @classmethod
    def _get_class(cls) -> type[tio.Transform]:
        """Returns the transform associated to this config class."""
        return getattr(zoo_transforms, cls._get_name())
