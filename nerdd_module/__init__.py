from .cli import *
from .model import *
from .output import *
from .polyfills import get_entry_points
from .problem import *
from .version import *

for entry_point in get_entry_points("nerdd-module.plugins"):
    entry_point.load()
