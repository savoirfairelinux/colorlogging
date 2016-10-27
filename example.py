import logging
import colorlogging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

format = "%(asctime)s %(levelname)s: #(magenta)%(message)s#(plain)"
formatter = colorlogging.ColorFormatter(format)
handler.setFormatter(formatter)

logger.info('This will be printed in magenta!')

format = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = colorlogging.ColorFormatter()
formatter.setLevelColor(logging.INFO, 'magenta')
handler.setFormatter(formatter)

logger.info('#(green)This message will be printed in green!#(plain)')