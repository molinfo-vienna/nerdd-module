from nerdd_module import Model


class BrokenConfigModel(Model):
    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        for _ in mols:
            yield {}

    def _get_base_config(self):
        raise ValueError("Broken configuration for testing purposes")


def test_broken_config_is_detected_in_predict():
    model = BrokenConfigModel()
    try:
        model.predict([])
    except ValueError:
        assert True, "Expected ValueError due to broken configuration"
        return

    raise AssertionError("Expected ValueError due to broken configuration not raised")
