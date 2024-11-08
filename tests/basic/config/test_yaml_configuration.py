from pathlib import Path

from nerdd_module.config import YamlConfiguration

here = Path(__file__).parent


def test_mimetype_svg():
    c = YamlConfiguration(here / "data" / "mimetype_svg.yaml")
    logo = c.get_dict()["logo"]
    assert logo.startswith("data:image/svg+xml;base64,")
