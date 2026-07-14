"""Configuration layer: typed settings, logging, and (later) the DI container."""

from copilot.config.logging import configure_logging, get_logger
from copilot.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings", "configure_logging", "get_logger"]
