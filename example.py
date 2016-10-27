import logging
from colorlogging import ColorFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

fmt = "%(asctime)s %(levelname)s: #(magenta)%(message)s#(plain)"
formatter = ColorFormatter(fmt)
handler.setFormatter(formatter)

logger.info('This will be printed in magenta!')
logger.info('#(underlined green)This message will be underlined and green!')

fmt = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = ColorFormatter(fmt)
formatter.setLevelColor(logging.INFO, 'inverted light cyan')
handler.setFormatter(formatter)
logger.info('Nothing to see, just a humble log message.')

formatter = ColorFormatter(additive=True)
handler.setFormatter(formatter)
logger.info('#(bold)This is bold. #(blue)This is bold and blue. #(not bold)This is only blue.')

formatter = ColorFormatter()  # additive is False by default
handler.setFormatter(formatter)
logger.info('#(bold)This is bold. #(blue)This is only blue, not bold.')
