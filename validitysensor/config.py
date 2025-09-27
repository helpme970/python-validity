#!/usr/bin/env python3

"""
Configuration module for python-validity fingerprint sensor.
"""

import os
import configparser
import logging
from pathlib import Path

class Config:
    """Configuration manager for python-validity."""
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = self._get_config_file()
        self._load_defaults()
        self._load_config()
    
    def _get_config_file(self):
        """Get the configuration file path."""
        # Try system config first
        system_config = Path('/etc/python-validity/config.ini')
        if system_config.exists():
            return system_config
        
        # Try user config
        user_config_dir = Path.home() / '.config' / 'python-validity'
        user_config_dir.mkdir(parents=True, exist_ok=True)
        user_config = user_config_dir / 'config.ini'
        
        return user_config
    
    def _load_defaults(self):
        """Load default configuration values."""
        self.config['scanning'] = {
            'base_interval': '0.5',
            'max_interval': '3.0',
            'adaptive_polling': 'true',
            'adaptive_threshold': '5',
            'error_cooldown': '5.0',
            'lockscreen_optimization': 'true',
            'pause_on_timeout': 'false',
            'pause_timeout': '30.0',
            'input_detection_method': 'auto'
        }
        
        self.config['logging'] = {
            'level': 'INFO',
            'adaptive_debug': 'false'
        }
    
    def _load_config(self):
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                self.config.read(self.config_file)
                logging.debug(f'Loaded configuration from {self.config_file}')
            except Exception as e:
                logging.warning(f'Error loading config file {self.config_file}: {e}')
    
    def save_default_config(self):
        """Save the default configuration to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            logging.info(f'Default configuration saved to {self.config_file}')
        except Exception as e:
            logging.error(f'Error saving config file {self.config_file}: {e}')
    
    def get_float(self, section, key, fallback=None):
        """Get a float value from configuration."""
        try:
            return self.config.getfloat(section, key, fallback=fallback)
        except (ValueError, TypeError):
            logging.warning(f'Invalid float value for {section}.{key}, using fallback')
            return fallback
    
    def get_int(self, section, key, fallback=None):
        """Get an integer value from configuration."""
        try:
            return self.config.getint(section, key, fallback=fallback)
        except (ValueError, TypeError):
            logging.warning(f'Invalid int value for {section}.{key}, using fallback')
            return fallback
    
    def get_bool(self, section, key, fallback=None):
        """Get a boolean value from configuration."""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except (ValueError, TypeError):
            logging.warning(f'Invalid bool value for {section}.{key}, using fallback')
            return fallback
    
    def get_str(self, section, key, fallback=None):
        """Get a string value from configuration."""
        return self.config.get(section, key, fallback=fallback)

# Global configuration instance
config = Config()

# Scanning configuration
SCAN_BASE_INTERVAL = config.get_float('scanning', 'base_interval', 0.5)
SCAN_MAX_INTERVAL = config.get_float('scanning', 'max_interval', 3.0)
ADAPTIVE_POLLING_ENABLED = config.get_bool('scanning', 'adaptive_polling', True)
ADAPTIVE_THRESHOLD = config.get_int('scanning', 'adaptive_threshold', 5)
ERROR_COOLDOWN = config.get_float('scanning', 'error_cooldown', 5.0)
LOCKSCREEN_OPTIMIZATION = config.get_bool('scanning', 'lockscreen_optimization', True)

# Logging configuration
LOG_LEVEL = config.get_str('logging', 'level', 'INFO')
ADAPTIVE_DEBUG = config.get_bool('logging', 'adaptive_debug', False)

# Pause/Resume configuration
PAUSE_ON_TIMEOUT = config.get_bool('scanning', 'pause_on_timeout', False)
PAUSE_TIMEOUT = config.get_float('scanning', 'pause_timeout', 30.0)
INPUT_DETECTION_METHOD = config.get_str('scanning', 'input_detection_method', 'auto')
