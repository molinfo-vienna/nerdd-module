import pkg_resources

from .abstract_model import *
from .cli import *
from .config import *
from .version import *

for entry_point in pkg_resources.iter_entry_points("nerdd-module.plugins"):
    entry_point.load()
