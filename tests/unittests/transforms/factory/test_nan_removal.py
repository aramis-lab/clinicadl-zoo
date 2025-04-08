import pytest
import torch
import torchio as tio
from clinicadl.data.structures import DataPoint

from clinicadl_zoo.transforms import NanRemoval
from clinicadl_zoo.transforms.config import NanRemovalConfig
from clinicadl_zoo.transforms.factory import get_transform_config

GOOD_INPUTS = [
    {"posinf": 1.2, "neginf": 0.1},
    {"posinf": None, "neginf": None},
]


@pytest.mark.parametrize("args", GOOD_INPUTS)
def test_good_inputs(args: dict):
    config = NanRemoval(**args)
    for arg, value in args.items():
        assert getattr(config, arg) == value


def test_get_object():
    config = NanRemovalConfig()
    transform_from_config = config.get_object()
    assert isinstance(transform_from_config, NanRemoval)


def test_nan_removal():
    img = torch.zeros(1, 4, 5, 3)
    label = torch.ones(1, 4, 5, 3)

    label[0, 0, 0, 0] = torch.nan

    img[0, 0, 0, 0] = torch.nan
    img[0, 1, 1, 0] = torch.inf
    img[0, 1, 0, 0] = -torch.inf

    data = DataPoint(
        image=tio.ScalarImage(tensor=img),
        label=tio.LabelMap(tensor=label),
        participant="",
        session="",
    )

    transform = NanRemoval()
    transformed = transform(data)
    assert transformed.image.tensor[0, 0, 0, 0] == 0
    assert transformed.image.tensor[0, 1, 1, 0] == torch.finfo().max
    assert transformed.image.tensor[0, 1, 0, 0] == torch.finfo().min
    assert transformed.label.tensor[0, 0, 0, 0].isnan()

    transform = NanRemoval(nan=1, posinf=1, neginf=-1)
    transformed = transform(data)
    assert transformed.image.tensor[0, 0, 0, 0] == 1
    assert transformed.image.tensor[0, 1, 1, 0] == 1
    assert transformed.image.tensor[0, 1, 0, 0] == -1


def test_factory():
    config = get_transform_config("NanRemoval", nan=1)
    assert config.name == "NanRemoval"
    assert config.nan == 1
    assert config.posinf is None
    assert config.neginf is None
