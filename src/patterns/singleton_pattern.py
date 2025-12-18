"""
Singleton Pattern - Creational Design Pattern
Ensures a class has only one instance and provides a global point of access
"""
from typing import Optional


class ConfigurationManager:
    """
    Singleton configuration manager
    Demonstrates Singleton Pattern
    """
    _instance: Optional['ConfigurationManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._config = {
                'app_name': 'E-Commerce System',
                'version': '1.0.0',
                'max_items_per_order': 50,
                'default_currency': 'USD',
                'tax_rate': 0.08
            }
            ConfigurationManager._initialized = True
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value) -> None:
        """Set configuration value"""
        self._config[key] = value
    
    def get_all(self) -> dict:
        """Get all configuration values"""
        return self._config.copy()


def get_config() -> ConfigurationManager:
    """Get the singleton instance of configuration manager"""
    return ConfigurationManager()
