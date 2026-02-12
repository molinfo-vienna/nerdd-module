import logging
from threading import RLock

from .polyfills import get_entry_points

logger = logging.getLogger(__name__)

_plugins_loaded = False
_plugins_loading = False
_plugins_lock = RLock()


def ensure_plugins_loaded() -> None:
    global _plugins_loaded, _plugins_loading

    with _plugins_lock:
        if _plugins_loaded or _plugins_loading:
            return

        _plugins_loading = True
        try:
            for entry_point in get_entry_points("nerdd_module.plugins"):
                try:
                    entry_point.load()
                except Exception as error:
                    entry_point_name = getattr(entry_point, "name", "unknown")
                    logger.error("Failed to load plugin %r: %s", entry_point_name, error)
            _plugins_loaded = True
        finally:
            _plugins_loading = False
