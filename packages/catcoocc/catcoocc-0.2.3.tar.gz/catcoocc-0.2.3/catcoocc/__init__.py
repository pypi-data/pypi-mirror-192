# __init__.py

# Informatin on the package
__version__ = "0.2.3"
__author__ = "Tiago Tresoldi"
__email__ = "tiago.tresoldi@lingfil.uu.se"

# Build the namespace
from catcoocc.utils import *
from catcoocc import scorer
from catcoocc import correlation

# Resource dir (mostly for tests)
from pathlib import Path

RESOURCE_DIR = Path(__file__).parent.parent / "resources"
