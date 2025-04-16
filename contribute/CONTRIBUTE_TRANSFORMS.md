- [STEP 1: Write the Transform](#step-1-write-the-transform)
- [STEP 2: Add the name of your transform in the list](#step-2-add-the-name-of-your-transform-in-the-list)
- [STEP 3: Create the config class associated to your transform](#step-3-create-the-config-class-associated-to-your-transform)
- [STEP 4: Test your code](#step-4-test-your-code)
- [STEP 5: Create a Pull Request in the repository ](#step-5-create-a-pull-request-in-the-repository)
- [STEP 6: Use your transform in ClinicaDL!](#step-6-use-your-transform-in-clinicadl)

<br>

# How to add your own transforms in the ClinicaDL Transforms Zoo?

The goal of this tutorial is to add your own transforms to the ClinicaDL Transform Zoo, so that they benefit the community and can be easily reused in your future works.

For this tutorial, you will work on the Git repository [ClinicaDL Zoo](https://github.com/aramis-lab/clinicadl-zoo.git). You can clone it via:

```
git clone https://github.com/aramis-lab/clinicadl-zoo.git
```

And then create a new branch and go to this branch:

```
git checkout -b my_custom_transform
```

## STEP 1: Write the Transform

First of all, add your transform in a Python file in `clinicadl_zoo/transforms/transforms`.

To write a transform compatible with ClinicaDL, please follow the [associated tutorial](https://github.com/aramis-lab/clinicadl-tutorials/blob/main/transforms/custom_transforms.ipynb).

<u>In a nutshell</u>:

A transform compatible with ClinicaDL is a transform that inherits from [torchio.Transforms](https://torchio.readthedocs.io/transforms/transforms.html#torchio.transforms.Transform). 

You only need to overwrite the ``__init__``, where you define your parameters (don't forget to define the list of these parameters is ``self.arg_names``), and the method ``apply_transform``, where you actually compute the transform.

This latter must take as input and return a [DataPoint](https://clinicadl.readthedocs.io/en/latest/data/datapoint.html#clinicadl.data.structures.DataPoint). Inside, feel free to use the useful methods of DataPoint to compute your transforms. You will likely be particularly interested in ``get_images``, that enables you to iterate on all the images and masks in the DataPoint.

PS: don't forget to call ``super().__init__()``!

```python
# in clinicadl_zoo/transforms/transforms/my_custom_transform.py

import torchio as tio
from clinicadl.data.structures import DataPoint


class MyCustomTransform(tio.Transform):
    """
    The description of your transform.

    Parameters
    ----------
    arg1 : float
        Description of arg1.
    arg2 : int (default=0)
        Description of arg2.
    """

    def __init__(
        self,
        arg1: float,
        arg2: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.arg1, self.arg2 = arg1, arg2
        self.args_names = ["arg1", "arg2"]

    def apply_transform(self, datapoint: DataPoint) -> DataPoint:  # pylint: disable=arguments-renamed
        """
        Apply the transform to the datapoint.
        """
        return datapoint
```

Then, add this transform in ``clinicadl_zoo/transforms/transforms/__init__``:

```python
# in clinicadl_zoo/transforms/transforms/__init__.py

from .my_custom_transform import MyCustomTransform
from .nan_removal import NanRemoval
from .template import Template
```

## STEP 2: Add the name of your transform in the list

Then, you need to add the name of your transform in the ``ZooTransform`` enum in the `clinicadl_zoo.transforms.enum`.

```python
# in clinicadl_zoo/transforms/enum.py

class ZooTransform(str, BaseEnum):
    """
    Implemented transforms in ClinicaDL Transform Zoo.
    """

    MY_CUSTOM_TRANSFORM = "MyCustomTransform"
    NAN_REMOVAL = "NanRemoval"
    TEMPLATE = "Template"
```

## STEP 3: Create the config class associated to your transform

ClinicaDL uses **configuration classes** to easily manipulate objects from different Deep Learning libraries and to enhance the reproducibility of your code.

So, when you implement a new transform in ClinicaDL Zoo, we ask you to also create the associated configuration class.

This class must inherit from `ZooTransformConfig` (in `clinicadl_zoo.transforms.config.base`) and **must be named like the transform, followed by the suffix "Config"**.

```python
# in clinicadl_zoo/transforms/config/my_custom_transform.py

from typing import Union

from clinicadl.utils.config import DefaultFromLibrary

from .base import ZooTransformConfig


class MyCustomTransformConfig(ZooTransformConfig):
    """
    Config class for :py:class:`clinicadl_zoo.transforms.MyCustomTransform`.
    """

    arg1: float
    arg2: int

    def __init__(
        self,
        arg1: float,
        arg2: Union[int, DefaultFromLibrary] = DefaultFromLibrary.YES,
    ):
        super().__init__(arg1=arg1, arg2=arg2)
```

Notice that for arguments that are optional in ``MyCustomTransform``, we use the ``DefaultFromLibrary`` tool. Basically, it means here that if the user doesn't pass any value for ``arg2``, ``MyCustomTransformConfig`` will use the default value for ``arg2`` in ``MyCustomTransform``.

```python
>>> MyCustomTransformConfig(arg1=1.0)
MyCustomTransformConfig(arg1=1.0, arg2=0 name='MyCustomTransform')
```

Then add this configuration class in ``clinicadl_zoo/transforms/config/__init__``:

```python
# in clinicadl_zoo/transforms/transforms/__init__.py

from .my_custom_transform import MyCustomTransformConfig
from .nan_removal import NanRemovalConfig
from .template import TemplateConfig
```

## STEP 4: Test your code

Good coding practices require that you test the code you have just implemented. Put your unittests in ``tests/unittests/transforms/factory/test_my_custom_transform.py``. Have a look at an example in [tests/unittests/transforms/factory/test_nan_removal.py](https://github.com/aramis-lab/clinicadl-zoo/blob/main/tests/unittests/transforms/factory/test_nan_removal.py) to help you.

Once the tests are implemented, you can test your code with the command:

```
pytest tests/unittests/transform
```

PS: before running this command, make sure that your `clinicadl` environment is activated and that you are
the repo `clinicadl-zoo`.

## STEP 5: Create a Pull Request in the repository 

Once everything is implemented and tested, you should open a pull request on the ``main`` branch of this repository.

Make sure to briefly describe your transform, its purpose, and the parameters it introduces. This helps the maintainers to review and integrate your contribution more efficiently.

If you have any questions or run into issues during the process, don’t hesitate to [contact us](https://github.com/aramis-lab/clinicadl-zoo/issues) — we’re happy to help!

## STEP 6: Use your transform in ClinicaDL!

Once your Pull Request has been merged into the ``main`` branch, go back to your ``clinicadl`` repository, checkout to ``clinicadl_v2``, and update your environment:

```
poetry install --extras zoo
```

Then, use your transform like any other transform supported in ClinicaDL!

```python
from clinicadl_zoo.transforms.config import MyCustomTransformConfig
from clinicadl.transforms.config import ZNormalizationConfig
from clinicadl.transforms import Transforms

transforms = Transforms(image_transforms=[MyCustomTransformConfig(arg1=1.0), ZNormalizationConfig()])
transforms.get_transforms()[0]
>>> Compose([MyCustomTransform(arg1=1.0, arg2=0), ZNormalization(masking_method=None)])
```