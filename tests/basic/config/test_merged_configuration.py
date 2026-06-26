from nerdd_module.config import DictConfiguration, MergedConfiguration


def test_job_parameters_are_none():
    d1 = DictConfiguration({"name": "test", "job_parameters": None})
    d2 = DictConfiguration({"job_parameters": []})

    c = MergedConfiguration(d1, d2)

    config = c.get_dict()

    assert (
        isinstance(config.job_parameters, list) and len(config.job_parameters) == 0
    ), "Expected job_parameters to be an empty list"
