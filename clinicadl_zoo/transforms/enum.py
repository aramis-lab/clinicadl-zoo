from clinicadl.utils.enum import BaseEnum


class ZooTransform(str, BaseEnum):
    """
    Implemented transforms in ClinicaDL Transform Zoo.
    """

    NAN_REMOVAL = "NanRemoval"
    TEMPLATE = "Template"
