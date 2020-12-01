"""logging configuration"""
from config_loader import load_config
from typing import Any, Dict


class LogConfig:
    """Logging related configuration

    Attributes:
        log_level (str): python logging level
        log_location (str): log file output location
    """
    _lcfg: Dict[Any, Any] = load_config('logging')
    log_level: str = _lcfg['log_level']
    log_location: str = _lcfg['log_location']
