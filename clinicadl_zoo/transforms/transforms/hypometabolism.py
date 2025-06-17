from copy import deepcopy
from pathlib import Path
from typing import Union

import nibabel as nib
import numpy as np
import torchio as tio
from clinicadl.data.structures import DataPoint
from scipy.ndimage import gaussian_filter


class Hypometabolism(tio.IntensityTransform):
    """
    To simulate dementia-related hypometabolism, aimed to be used on FDG PET images.
    This transform reduces the intensity of signal in specific brain regions based on the mask of a pathology.

    Ref. https://www.melba-journal.org/papers/2024:003.html.

    Parameters
    ----------
    mask_dir : str or Path
        Directory containing the mask files.
    pathology : str
        Type of pathology to simulate (e.g., "AD", "bvFTD").
    percentage : int
        Percentage of hypometabolism to apply.
        The value should be between 0 and 100.
        0 means no hypometabolism, while 100 means complete removal of the signal in the masked regions.
    sigma : int, optional
        Standard deviation for Gaussian noise, by default 2.
    """

    def __init__(
        self,
        mask_dir: Union[str, Path],
        pathology: str,
        percentage: int,
        sigma: int = 2,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")

        self.mask_dir = mask_dir
        self.pathology = pathology
        self.percentage = percentage
        self.sigma = sigma

        mask_path = Path(
            self.mask_dir, f"mask_hypo_{self.pathology.lower()}_resampled.nii"
        )
        if not mask_path.is_file():
            raise FileNotFoundError(
                f"Mask file for pathology '{self.pathology}' not found at {mask_path}."
            )
        mask_nii = nib.load(mask_path)
        self.mask = self._mask_processing(mask_nii.get_fdata())

        self.args_names = ["mask_dir", "pathology", "percentage", "sigma"]

    def apply_transform(self, datapoint: DataPoint) -> DataPoint:  # pylint: disable=arguments-renamed
        """
        Apply the transform to the datapoint.
        """
        transformed = deepcopy(datapoint)

        for image in transformed.get_images(intensity_only=True):
            image.tensor[:] *= self.mask

        transformed.add_image(datapoint.image, "original_image")
        transformed.add_mask(
            tio.LabelMap(
                tensor=np.expand_dims(self.mask, axis=0), affine=datapoint.image.affine
            ),
            "hypo_mask",
        )
        transformed["pathology"] = self.pathology
        transformed["percentage"] = self.percentage

        return transformed

    def _mask_processing(self, mask: np.array) -> np.array:
        inverse_mask = 1 - mask
        inverse_mask[inverse_mask == 0] = 1 - self.percentage / 100
        gaussian_mask = gaussian_filter(inverse_mask, sigma=self.sigma)
        return np.float32(gaussian_mask)
