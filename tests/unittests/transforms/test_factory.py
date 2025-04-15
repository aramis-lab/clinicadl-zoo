from clinicadl_zoo.transforms.factory import get_transform_config


def test_factory():
    config = get_transform_config("NanRemoval", nan=1)
    assert config.name == "NanRemoval"
    assert config.nan == 1
    assert config.posinf is None
    assert config.neginf is None
