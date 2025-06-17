import os
from pathlib import Path

import nibabel as nib
import numpy as np
import torch
import torchio as tio
from clinicadl.data.structures import DataPoint

from clinicadl_zoo.transforms import Hypometabolism
from clinicadl_zoo.transforms.config import HypometabolismConfig


def build_mask() -> Path:
    mask = torch.zeros(4, 5, 3)
    mask[0, 0, 0] = 1
    mask[1, 1, 0] = 1
    mask[1, 0, 0] = 1
    print(mask)
    nifti = nib.Nifti1Image(mask.numpy(), np.eye(4))
    tmp_mask_path = Path(__file__).parents[2] / "tmp/mask_hypo_ad_resampled.nii"
    os.makedirs(tmp_mask_path.parent, exist_ok=True)
    nib.save(nifti, tmp_mask_path)
    return tmp_mask_path


def remove_mask(tmp_mask_path: Path):
    if tmp_mask_path.is_file():
        tmp_mask_path.unlink()
    os.removedirs(tmp_mask_path.parent)


def test_get_object():
    tmp_mask_path = build_mask()
    config = HypometabolismConfig(
        mask_dir=tmp_mask_path.parent,
        pathology="AD",
        percentage=30,
    )
    hypometabolism = config.get_object()
    assert isinstance(hypometabolism, Hypometabolism)


def test_hypometabolism():
    tmp_mask_path = build_mask()

    img = torch.ones(1, 4, 5, 3)

    data = DataPoint(
        image=tio.ScalarImage(tensor=img),
        label=None,
        participant="",
        session="",
    )

    transform = Hypometabolism(
        mask_dir=tmp_mask_path.parent, pathology="AD", percentage=30, sigma=0
    )
    transformed = transform(data)

    assert transformed.image.tensor[0, 0, 0, 0] == 0.7
    assert transformed.image.tensor[0, 1, 1, 0] == 0.7
    assert transformed.image.tensor[0, 1, 0, 0] == 0.7
    assert transformed.image.tensor[0, 0, 0, 1] == 1

    transform = Hypometabolism(
        mask_dir=tmp_mask_path.parent, pathology="AD", percentage=70, sigma=0
    )
    transformed = transform(data)

    assert transformed.image.tensor[0, 0, 0, 0] == 0.3
    assert transformed.image.tensor[0, 1, 1, 0] == 0.3
    assert transformed.image.tensor[0, 1, 0, 0] == 0.3
    assert transformed.image.tensor[0, 0, 0, 1] == 1

    remove_mask(tmp_mask_path)
