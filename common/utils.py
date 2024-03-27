import sys
import yaml
from dynaconf import Dynaconf

def load_config(file_path: str) -> dict:
    config = Dynaconf(settings_files=[file_path])
    return config
