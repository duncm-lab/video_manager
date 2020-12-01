"""load settings from config file"""
import yaml
import os

path = os.path.dirname(os.path.abspath(__file__))


def load_config(config_section: str) -> dict:
    """Read settings from config.yml
    Args:
        config_section (str): config group key

    Returns:
        dict: configuration settings
    """
    with open(os.path.join(path, 'config.yml'), 'r') as fl:
        cfg = yaml.safe_load(fl.read())
    return cfg[config_section]
