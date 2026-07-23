import logging

from nerdd_module import _plugins
from nerdd_module.output import Writer


class EntryPoint:
    def __init__(self, name, load):
        self.name = name
        self.load = load


def test_plugins_are_loaded_once(monkeypatch):
    loaded = []
    monkeypatch.setattr(
        _plugins,
        "get_entry_points",
        lambda group: [EntryPoint("test", lambda: loaded.append(group))],
    )
    monkeypatch.setattr(_plugins, "_plugins_loaded", False)
    monkeypatch.setattr(_plugins, "_plugins_loading", False)

    _plugins.ensure_plugins_loaded()
    _plugins.ensure_plugins_loaded()

    assert loaded == ["nerdd_module.plugins"]


def test_plugin_load_errors_are_logged_and_do_not_block_other_plugins(monkeypatch, caplog):
    loaded = []

    def fail():
        raise RuntimeError("broken plugin")

    monkeypatch.setattr(
        _plugins,
        "get_entry_points",
        lambda group: [
            EntryPoint("broken", fail),
            EntryPoint("working", lambda: loaded.append(group)),
        ],
    )
    monkeypatch.setattr(_plugins, "_plugins_loaded", False)
    monkeypatch.setattr(_plugins, "_plugins_loading", False)

    with caplog.at_level(logging.ERROR, logger="nerdd_module._plugins"):
        _plugins.ensure_plugins_loaded()

    assert loaded == ["nerdd_module.plugins"]
    assert "Failed to load plugin 'broken': broken plugin" in caplog.messages


def test_writer_registry_loads_plugins_on_first_use(monkeypatch):
    loaded = []
    monkeypatch.setattr(
        _plugins,
        "get_entry_points",
        lambda group: [EntryPoint("test", lambda: loaded.append(group))],
    )
    monkeypatch.setattr(_plugins, "_plugins_loaded", False)
    monkeypatch.setattr(_plugins, "_plugins_loading", False)

    Writer.get_output_formats()

    assert loaded == ["nerdd_module.plugins"]
