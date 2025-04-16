import numpy as np
import pytest
import torch
import torchio as tio
from clinicadl.data.structures import DataPoint
from pydantic import ValidationError

from clinicadl_zoo.transforms import NanRemoval
from clinicadl_zoo.transforms.config import NanRemovalConfig

BAD_INPUTS = [{"nan": None}]
GOOD_INPUTS = [
    {"nan": 1.42, "posinf": 1.2, "neginf": 0.1},
    {"posinf": None, "neginf": None},
]


@pytest.mark.parametrize("args", BAD_INPUTS)
def test_bad_inputs(args: dict):
    with pytest.raises(ValidationError):
        NanRemovalConfig(**args)


@pytest.mark.parametrize("args", GOOD_INPUTS)
def test_good_inputs(args: dict):
    config = NanRemovalConfig(**args)
    for arg, value in args.items():
        assert getattr(config, arg) == value


def test_get_object():
    config = NanRemovalConfig(posinf=1.2)
    nan_removal = config.get_object()
    assert isinstance(nan_removal, NanRemoval)
    assert np.isclose(nan_removal.posinf, 1.2)
    assert nan_removal.neginf is None  # default


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
