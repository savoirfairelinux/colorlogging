"""
A simple colored loggging module.

Attributes:
    COLORS (tuple): list of available colors and styles
    DEFAULT_FORMAT (str): default format string for ColorFormatter

Example:
    ``
    import logging
    import colorlogging

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    format = '#(level)$(levelname)s#(plain): #(cyan)%(message)s'

    formatter = colorlogging.ColorFormatter(format)
    handler.setFormatter(formatter)

    logger.info('This message will be printed in cyan')
    logger.info('#(blue)This message will be printed in blue')
    ``

    ``level`` is a special color name that prints a different color
    depending on the level of the message. A typical use case would
    be coloring the levelname.

    There are default colors associated with the default levels:
    INFO, WARN, etc. They can be changed, and new levels can be added, with
    the ``setLevelColor`` method.
"""
from .core import ColorFormatter, COLORS, DEFAULT_FORMAT
