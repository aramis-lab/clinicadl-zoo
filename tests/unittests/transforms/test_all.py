import torch
import torchio as tio
from clinicadl.data.structures import DataPoint
from clinicadl.transforms.config import TransformConfig

from clinicadl_zoo.transforms import ZooTransform
from clinicadl_zoo.transforms.factory import get_transform_config

X = DataPoint(
    image=tio.ScalarImage(tensor=torch.randn(1, 16, 17, 18)),
    label=tio.LabelMap(tensor=torch.ones(1, 16, 17, 18)),
    participant="",
    session="",
)


def test_get_transform_config():
    config = get_transform_config("NanRemoval", nan=1)
    assert config.name == "NanRemoval"
    assert config.nan == 1
    assert config.posinf is None
    assert config.neginf is None


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
        assert isinstance(transform_obj(X), DataPoint)
