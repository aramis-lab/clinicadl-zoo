import pytest
import torch
import torchio as tio
from clinicadl.transforms.config import TransformConfig

from clinicadl_zoo.transforms import ZooTransform
from clinicadl_zoo.transforms.factory import get_transform_config

X = tio.Subject(
    image=tio.ScalarImage(tensor=torch.randn(1, 16, 17, 18)),
    label=tio.LabelMap(tensor=torch.ones(1, 16, 17, 18)),
)


def test_all_config():
    """
    Check that all transforms are implemented in the zoo.
    """
    for transform in ZooTransform:
        config = get_transform_config(transform.value)
        assert config is not None
        assert isinstance(config, TransformConfig)
        assert "name" in config.model_dump()
        assert config.name == transform.value
        hasattr(type[config], "_get_class")


def test_all_transforms():
    """
    Check that all transforms are implemented in the zoo.
    """
    for transform in ZooTransform:
        config = get_transform_config(transform.value)
        transform_type = config._get_class()
        assert issubclass(transform_type, tio.Transform)

        transform_obj = config.get_object()
        assert isinstance(transform_obj, tio.Transform)
        assert isinstance(transform_obj(X), tio.Subject)
