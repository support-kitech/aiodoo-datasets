"""Central logging abstraction for the Execution Generator."""

import logging

def get_logger(name: str) -> logging.Logger:
    """
    Get a pre-configured logger for the given module name.
    
    Args:
        name: The module name (usually `__name__`).
        
    Returns:
        A configured logging instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def set_log_level(level: int) -> None:
    """Set the global log level."""
    logging.getLogger().setLevel(level)
