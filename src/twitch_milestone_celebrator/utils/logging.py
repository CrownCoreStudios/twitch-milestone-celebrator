"""Logging configuration and utilities for the Twitch Milestone Celebrator."""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from twitch_milestone_celebrator.config.settings import LoggingConfig


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels."""
    
    # ANSI color codes
    GREY = "\x1b[38;21m"
    BLUE = "\x1b[38;5;39m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: f"{GREY}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.INFO: f"{BLUE}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.WARNING: f"{YELLOW}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.ERROR: f"{RED}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.CRITICAL: f"{BOLD_RED}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(
    name: str = "twitch_milestone_celebrator",
    log_level: Optional[str] = None,
    log_file: Optional[Path] = None,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name: Name of the logger
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup log files to keep
        
    Returns:
        Configured logger instance
    """
    # Get logger
    logger = logging.getLogger(name)
    
    # Don't propagate to root logger
    logger.propagate = False
    
    # Set log level
    if log_level is None:
        log_level = LoggingConfig.LOG_LEVEL
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if log_file is None:
        log_file = LoggingConfig.LOG_FILE
    
    try:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
    except (PermissionError, OSError) as e:
        logger.warning("Failed to set up file logging: %s", str(e), exc_info=True)
    
    return logger


# Create default logger instance
logger = setup_logger()


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Name of the logger. If None, returns the root logger.
        
    Returns:
        Logger instance
    """
    if name is None:
        return logging.getLogger()
    return logging.getLogger(f"twitch_milestone_celebrator.{name}")
