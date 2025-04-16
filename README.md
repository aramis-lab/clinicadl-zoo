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

- [add a transform](contribute/CONTRIBUTE_TRANSFORMS.md)

### Prerequisite

To contribute, you need:

1. a [Python environment with ClinicaDL](https://clinicadl.readthedocs.io/en/latest/installation.html) installed;
2. to clone this repository (ideally, [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) it first):

    ```
    git clone https://github.com/aramis-lab/clinicadl-zoo.git
    ```
3. to install some developing tools:
    ```
    cd clinicadl-zoo
    pip install pre-commit
    pre-commit install
    ```