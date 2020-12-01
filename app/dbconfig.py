"""Mongo database connection"""
from config_loader import load_config
from typing import Any, Dict


class DBConfig:
    """Database related configuration

    Attributes:
        mongo_server (str): server host
        mongo_database (str): mongo database name
        mongo_collection (str): mongo collection name
    """
    _lcfg: Dict[Any, Any] = load_config('mongo_db')

    mongo_server: str = _lcfg['mongo_server']
    mongo_database: str = _lcfg['mongo_database']
    mongo_collection: str = _lcfg['mongo_collection']
