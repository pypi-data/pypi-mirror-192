from .io import yaml_load, yaml_dump, save, load, rm, json_load, json_dump
from .decorators import benchmark
from .string.color_string import rgb_string
from .functions.core import clamp
from .path import *
from .functions.core import topk, dict_topk
from .progress_bar import probar
from .performance import MeasureTime

_version_config = yaml_load("version-config.yaml", rel_path=True)
__version__ = _version_config["version"]
# print(f"{rgb_string(_version_config['name'], color='#34A853')} version: {rgb_string(__version__, color='#C9E8FF')}")
