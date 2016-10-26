import logging

COLORS = {
    'black': "\033[30m",
    'red': "\033[31m",
    'green': "\033[32m",
    'yellow': "\033[33m",
    'blue': "\033[34m",
    'magenta': "\033[35m",
    'cyan': "\033[36m",
    'light_gray': "\033[37m",
    'dark_gray': "\033[90m",
    'light_red': "\033[91m",
    'light_green': "\033[92m",
    'light_yellow': "\033[93m",
    'light_blue': "\033[94m",
    'light_magenta': "\033[95m",
    'light_cyan': "\033[96m",
    'white': "\033[97m",
    'bold': "\033[1m",
    'dim': "\033[2m",
    'underlined': "\033[4m",
    'blink': "\033[5m",
    'inverted': "\033[7m",
    'hidden': "\033[8m",
}


class ColorFormatter(logging.Formatter):
    DEFAULT_LVL_COLORS = None

    def __init__(self, *args, **kwargs):
        super(ColorFormatter, self).__init__(*args, **kwargs)
        self._lvl_colors = {}
        if self.DEFAULT_LVL_COLORS:
            for lvl, color in dict(self.DEFAULT_LVL_COLORS).items():
                self.setColor(lvl, color)

    def _parse_color_name(self, color_name):
        words = color_name.split(' ')
        try:
            code = ''.join(COLORS[word] for word in words)
        except KeyError:
            raise ValueError(
                'I don\'t know what color %s is. I know the colors: %s'
                % (color_name, COLORS.keys())
            )
        return code

    def setColor(self, lvl, color_name):
        code = self._parse_color_name(color_name)
        self._lvl_colors[lvl] = (color_name, code)

    @property
    def colors(self):
       return dict((k, self._lvl_colors[k][0]) for k in self._lvl_colors)

    def format(self, record):
        txt = super(ColorFormatter, self).format(record)
        if record.levelno in self._lvl_colors:
            color = self._lvl_colors[record.levelno][1]
        else:
            color = ""
        txt = txt.replace('$COLOR', color)
        txt = txt.replace('$ENDCOLOR', "\033[0m")
        return txt


def patch_logging():
    """
    Add SUCCESS and FAILURE log levels to logging.
    You probably don't want to use this.

    Adds the following:
        logging.SUCCESS
        logging.FAILURE
        logging.Logger.success()
        logging.Logger.failure()

    Those levels are colored green and red by default by ColorFormatter.
    They have levels close to INFO and ERROR, respectively.
    """
    SUCCESS = 19
    FAILURE = 39

    def success(self, *args, **kwargs):
        return self.log(SUCCESS, *args, **kwargs)

    def failure(self, *args, **kwargs):
        return self.log(FAILURE, *args, **kwargs)

    logging.Logger.success = success
    logging.Logger.failure = failure
    logging.addLevelName(SUCCESS, 'SUCCESS')
    logging.addLevelName(FAILURE, 'FAILURE')
    logging.SUCCESS = SUCCESS
    logging.FAILURE = FAILURE
    ColorFormatter.DEFAULT_LVL_COLORS = {
        SUCCESS: 'bold green',
        FAILURE: 'bold red',
    }


if __name__ == '__main__':
    patch_logging()
    handler = logging.StreamHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    formatter = ColorFormatter('%(levelname)s - $COLOR%(message)s$ENDCOLOR')
    handler.setFormatter(formatter)

    logger.success('this should be bold green')
    logger.failure('this should be bold red')
    logger.info('this should be gray')

    formatter.setColor(logging.INFO, 'yellow')
    logger.info('this should be yellow')

    formatter.setColor(logging.SUCCESS, 'underlined cyan')
    logger.success('this should be underlined cyan')

    formatter.setColor(logging.FAILURE, 'inverted light_magenta')
    logger.failure('this should look weird')

    formatter.setColor(logging.DEBUG, 'inverted bold blink blue')
    logger.debug('this might blink')

    from pprint import pprint
    pprint(formatter.colors)

