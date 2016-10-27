import copy
import logging
import re

COLORS = {
    'black': "\033[30m",
    'red': "\033[31m",
    'green': "\033[32m",
    'yellow': "\033[33m",
    'blue': "\033[34m",
    'magenta': "\033[35m",
    'cyan': "\033[36m",
    'light gray': "\033[37m",
    'gray': "\033[90m",
    'light red': "\033[91m",
    'light green': "\033[92m",
    'light yellow': "\033[93m",
    'light blue': "\033[94m",
    'light magenta': "\033[95m",
    'light cyan': "\033[96m",
    'white': "\033[97m",
    'bold': "\033[1m",
    'dim': "\033[2m",
    'underlined': "\033[4m",
    'blink': "\033[5m",
    'inverted': "\033[7m",
    'hidden': "\033[8m",
    'plain': "\033[0m",
    'default': "\033[0m",
    'normal': "\033[0m",
}


class ColorFormatter(logging.Formatter):
    _levelColors = {
        logging.CRITICAL: 'bold inverted red',
        logging.ERROR: 'bold red',
        logging.WARNING: 'bold yellow',
        logging.INFO: 'bold green',
        logging.DEBUG: 'bold blue',
    }

    def __init__(self, fmt=None, *args, **kwargs):
        if not fmt:
            fmt = '#(level)%(levelname)s#(plain): %(message)s'
        super(ColorFormatter, self).__init__(fmt, *args, **kwargs)
        self.levelColors = copy.deepcopy(self._levelColors)

    def _parse_color_name(self, color_name):
        words = color_name.split(' ')
        while ('light' in words):
            i = words.index('light')
            try:
                words = words[:i] + ['light ' + words[i+1]] + words[i+2:]
            except IndexError:
                raise ValueError('%s is not an accepted color.')
        try:
            code = ''.join(COLORS[word] for word in words)
        except KeyError:
            raise ValueError('%s is not an accepted color.')
        return code

    def setLevelColor(self, lvl, color):
        self.levelColors[lvl] = color

    re_color = re.compile(r'(\#\(([a-zA-Z][a-zA-Z ]*)\))')

    def format(self, record):
        txt = super(ColorFormatter, self).format(record)
        for match in self.re_color.finditer(txt):
            s, color = match.groups()
            if color == 'level':
                color = self.levelColors.get(record.levelno, 'plain')
            code = self._parse_color_name(color)
            txt = txt.replace(s, code, 1)
        return txt


if __name__ == '__main__':
    handler = logging.StreamHandler()
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    formatter = ColorFormatter()
    handler.setFormatter(formatter)

    logger.debug('#(magenta)this is a magenta debug message#(plain)')
    logger.info('this is an info message')
    logger.warn('this is a warning message')
    logger.error('this is an error message')
    logger.critical('this is a critical message')

    formatter.setLevelColor(logging.INFO, 'bold inverted cyan')
    logger.info('#(blink)this is a funky info message#(plain)')
