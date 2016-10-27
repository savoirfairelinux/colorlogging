import logging
import pprint

import colorlogging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

# Color/style modifiers can be added to format strings
fmt = "%(asctime)s %(levelname)s: #(magenta)%(message)s"
formatter = colorlogging.ColorFormatter(fmt)
handler.setFormatter(formatter)

logger.info('This will be printed in magenta!')

# They can also be added to messages
logger.info('#(underlined green)This message will be underlined and green!')

# level is a special color that depends on the log level
# The usual use case would be coloring the level name
# Note that #(plain) is used so that the message doesn't get styled
fmt = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = colorlogging.ColorFormatter(fmt)
handler.setFormatter(formatter)

# The standard log levels have default colors. INFO is green, WARN yellow, etc.
# setLevelColor can be used to modify the defaults,
formatter.setLevelColor(logging.INFO, 'inverted light cyan')
logger.info('Nothing to see, just a humble log message.')

# Or to add colors for custom log levels
formatter.setLevelColor(35, 'blink red')
logger.log(35, 'There are too many FOOs in your BARs')

# By default, style modifiers clear previous styles
formatter = colorlogging.ColorFormatter()
handler.setFormatter(formatter)
logger.info('#(bold)This is bold. #(blue)This is only blue, not bold.')

# This can be changed by setting the additive parameter
# If set to True, styles will be applied cumulatively
formatter = colorlogging.ColorFormatter(additive=True)
handler.setFormatter(formatter)
logger.info('#(bold)Bold. #(blue)Bold blue. #(not bold)Blue.')

# You can find the list of availabe style and colors in COLORS
pprint.pprint(colorlogging.COLORS)
