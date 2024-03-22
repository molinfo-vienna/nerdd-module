from .abstract_model import *
from .cli import *
from .config import *
from .problem import *
from .version import *

# import entry_points from importlib.metadata or fall back to pkg_resources
try:
    from importlib.metadata import entry_points

    def get_entry_points(group):
        return entry_points().get(group, [])

except ImportError:
    import pkg_resources

    def get_entry_points(group):
        return pkg_resources.iter_entry_points(group)


for entry_point in get_entry_points("nerdd-module.plugins"):
    entry_point.load()
