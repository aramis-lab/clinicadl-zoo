# ClinicaDL Zoo

ClinicaDL Zoo hosts a collection of transforms and models compatible with [ClinicaDL](https://github.com/aramis-lab/clinicadl).

Contributing to ``ClinicaDL Zoo`` will make your work fully compatible with ``ClinicaDL``, and thus
fully reproducible. It will also benefit the community.

## Getting started

Currently, ``ClinicaDL 2.0`` is in beta mode, so make sure you are on the branch ``clinicadl_v2`` and in the right [ClinicaDL environment](https://clinicadl.readthedocs.io/en/latest/installation.html), and run the command:

```
poetry install --extras zoo
````

> **_NOTE:_** In the future, ClinicaDL Zoo will be downloaded via: ```pip install clinicadl[zoo]```

Then, you can easily access all transforms and models in the zoo, and use
them in ``clinicadl``:

```python
>>> from clinicadl_zoo.transforms.config import NanRemovalConfig
>>> from clinicadl.transforms.config import ZNormalizationConfig
>>> from clinicadl.transforms import Transforms

>>> transforms = Transforms(image_transforms=[NanRemovalConfig(), ZNormalizationConfig()])
>>> transforms.get_transforms()[0]
Compose([NanRemoval(nan=0.0, posinf=None, neginf=None), ZNormalization(masking_method=None)])
```

## Contributing

To add your transforms or models to ``ClinicaDL Zoo``, you need to open
a Pull Request on this repository. To do this, please follow to relevant tutorial:

- [add a transform](https://github.com/aramis-lab/clinicadl-tutorials/blob/main/transforms/transforms_zoo.ipynb)