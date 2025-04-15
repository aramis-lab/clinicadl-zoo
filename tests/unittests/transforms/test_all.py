import inspect

import torch
import torchio as tio
from clinicadl.data.structures import DataPoint
from clinicadl.transforms import ImplementedTransform as TransformsInClinicaDL

import clinicadl_zoo.transforms.config as config_module
import clinicadl_zoo.transforms.transforms as transforms_module
from clinicadl_zoo.transforms import ZooTransform
from clinicadl_zoo.transforms.config.base import ZooTransformConfig

X = DataPoint(
    image=tio.ScalarImage(tensor=torch.randn(1, 16, 17, 18)),
    label=tio.LabelMap(tensor=torch.ones(1, 16, 17, 18)),
    participant="",
    session="",
)


def test_all_configs():
    """
    Check that all imported config classes in `transforms.config.__init__`
    inherit from TransformConfig.
    """
    for name in dir(config_module):
        cls = getattr(config_module, name)
        if inspect.isclass(cls):
            assert issubclass(cls, ZooTransformConfig), (
                f"All transform configs must inherit from "
                f"clinicadl_zoo.transforms.config.base.ZooTransformConfig. This is not the case for '{name}'."
            )
            assert issubclass(cls._get_class(), tio.Transform)
            assert cls._get_name() in [transform for transform in ZooTransform], (
                f"Cannot find the transform '{cls._get_name()}' (associated to '{name}' config) in clinicadl_zoo.transforms.enum.ZooTransform"
            )


def test_all_transforms():
    """
    Check that all transform classes in `transforms.transforms`:
    - inherit from tio.Transform
    - have an `apply_transform` method with correct signature
    """
    for name in dir(transforms_module):
        cls = getattr(transforms_module, name)
        if inspect.isclass(cls):
            assert issubclass(cls, tio.Transform), (
                f"All transforms must inherit from torchio.Transform. This is not the case for '{name}'."
            )
            assert not inspect.isabstract(cls), (
                f"All transforms must overwrite 'apply_transform' method. '{name}' does not."
            )
            assert name in [transform for transform in ZooTransform], (
                f"The name of your transform {name} must be in clinicadl_zoo.transforms.enum.ZooTransform."
            )

            # Check signature: takes exactly one argument (besides self)
            sig = inspect.signature(cls.apply_transform)
            assert sig.return_annotation is DataPoint, (
                f"{name}.apply_transform must return a DataPoint."
            )

            params = list(sig.parameters.values())
            assert len(params) == 2, (
                f"{name}.apply_transform must take one argument (besides self)."
            )

            param = params[1]
            assert param.annotation is not inspect.Parameter.empty, (
                f"{name}.apply_transform's argument must be type-annotated."
            )
            assert param.annotation is DataPoint, (
                f"{name}.apply_transform's argument must be of type DataPoint."
            )


def test_all_names():
    for name in [transform.value for transform in ZooTransform]:
        assert name not in [transform for transform in TransformsInClinicaDL], (
            f"Found a transform named '{name}' in clinicadl_zoo.transforms.enum.ZooTransform, "
            "but this name is already used in ClinicaDL."
        )
        assert hasattr(transforms_module, name), (
            f"'{name}' is in clinicadl_zoo.transforms.enum.ZooTransform but is not found in clinicadl_zoo.transforms.transforms.__init__"
        )
        config_name = f"{name}Config"
        assert hasattr(config_module, config_name), (
            f"'{name}' is in clinicadl_zoo.transforms.enum.ZooTransform but '{config_name}' is not found in clinicadl_zoo.transforms.config.__init__"
        )
