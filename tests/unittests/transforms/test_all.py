import inspect

import torch
import torchio as tio
from clinicadl.data.structures import DataPoint
from clinicadl.transforms.config import TransformConfig

import clinicadl_zoo.transforms.config as config_module
import clinicadl_zoo.transforms.transforms as transforms_module
from clinicadl_zoo.transforms.factory import get_transform_config

X = DataPoint(
    image=tio.ScalarImage(tensor=torch.randn(1, 16, 17, 18)),
    label=tio.LabelMap(tensor=torch.ones(1, 16, 17, 18)),
    participant="",
    session="",
)


def test_all_config():
    """
    Check that all imported config classes in `transforms.config.__init__`
    inherit from TransformConfig and have 'name' and '_get_class'.
    """
    for name in dir(config_module):
        cls = getattr(config_module, name)
        if inspect.isclass(cls):
            assert issubclass(cls, TransformConfig)
            assert not inspect.isabstract(cls)
            # assert isinstance(cls._get_class(), tio.Transform)  # TODO: uncomment when _get_class is a methodclass


def test_all_transforms():
    """
    Check that all transform classes in `transforms.transforms`:
    - inherit from tio.Transform
    - have an `args_names` attribute that is a list of str
    - have an `apply_transform` method with correct signature
    """
    for name in dir(transforms_module):
        cls = getattr(transforms_module, name)
        if inspect.isclass(cls):
            assert issubclass(cls, tio.Transform)

            # Check `apply_transform` method
            assert hasattr(
                cls, "apply_transform"
            ), f"{name} is missing 'apply_transform' method"
            method = getattr(cls, "apply_transform")
            assert callable(method), f"{name}.apply_transform is not callable"

            # Check signature: takes exactly one argument (besides self)
            sig = inspect.signature(method)
            assert sig.return_annotation is DataPoint

            params = list(sig.parameters.values())
            assert (
                len(params) == 2
            ), f"{name}.apply_transform must take one argument (besides self)"

            param = params[1]
            assert (
                param.annotation is not inspect.Parameter.empty
            ), f"{name}.apply_transform param must be type-annotated"
            assert (
                param.annotation is DataPoint
            ), f"{name}.apply_transform param must be of type DataPoint"


def test_factory():
    config = get_transform_config("NanRemoval", nan=1)
    assert config.name == "NanRemoval"
    assert config.nan == 1
    assert config.posinf is None
    assert config.neginf is None
