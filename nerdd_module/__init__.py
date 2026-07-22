import logging

from .cli import *
from .converters import *
from .model import *
from .output import *
from .polyfills import get_entry_points
from .problem import *
from .version import *

logger = logging.getLogger(__name__)

for entry_point in get_entry_points("nerdd_module.plugins"):
    try:
        entry_point.load()
    except Exception as e:
        entry_point_name = getattr(entry_point, "name", "unknown")
        logger.error("Failed to load plugin %r: %s", entry_point_name, e)
