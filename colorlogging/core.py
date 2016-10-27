"""Main file of colorlogging."""
import collections
import copy
import logging
import re
import sys


COLOR_CODES = {
    # Colors
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
    # Modifiers
    'bold': "\033[1m",
    'dim': "\033[2m",
    'underlined': "\033[4m",
    'blink': "\033[5m",
    'inverted': "\033[7m",
    'hidden': "\033[8m",
    # Undo modifiers
    'not bold': "\033[21m",
    'not dim': "\033[22m",
    'not underlined': "\033[24m",
    'not blink': "\033[25m",
    'not inverted': "\033[27m",
    'not hidden': "\033[28m",
    # Synonyms for clearing
    'plain': "\033[0m",
    'default': "\033[0m",
    'normal': "\033[0m",
}
COLORS = COLOR_CODES.keys()
IS_TTY = sys.stdout.isatty()
DEFAULT_FORMAT = '#(level)%(levelname)s#(plain): %(message)s'


class ColorFormatter(logging.Formatter):
    """
    Logging formatter with colored output.

    Add color annotations to log format strings and messages to produce styled,
    colored output for shells.

    See ``colorlogging.COLORS`` for available colors and styles. Colors and
    styles can be combined, for example 'bold red' is a valid style.

    Attributes:
        levelColors (dict): colors associated with log levels.

    Args:
        fmt (str): Format string for the message. In addition to the usual
            ``logging.Formatter`` syntax, supports color annotations like
            '#(blue)', '#(underlined red)'.
        datefmt (str): Format string for the date and time.
            (See logging.Formatter docs for more details.)
        autoclear (bool): Automatically add #(plain) at the end of messages.
            If ``autoclear`` is false, and #(plain) is omitted, the output
            will continue to be colored past the end of the message.
            Defaults to true.
        additive (bool): Apply color styles additively. Defaults to false.
            E.g., if true, '#(bold)#(blue)' will produce bold blue; if false,
            plain blue, since #(blue) was last. Note that in either case
            '#(bold blue)' will produce bold blue output.  Additive mode
            with negative modifiers, e.g. #(not bold) can be used for
            complex styling.
    """
    _levelColors = collections.defaultdict(
        lambda: 'plain',
        {
            logging.CRITICAL: 'bold inverted red',
            logging.ERROR: 'bold red',
            logging.WARNING: 'bold yellow',
            logging.INFO: 'bold green',
            logging.DEBUG: 'bold blue',
        }
    )

    def __init__(self, fmt=None, datefmt=None, additive=False, autoclear=True):
        fmt = fmt or DEFAULT_FORMAT
        super(ColorFormatter, self).__init__(fmt, datefmt)
        self.levelColors = copy.deepcopy(self._levelColors)
        self.additive = additive
        self.autoclear = autoclear

    def _join_word(self, words, to_join):
        while (to_join in words):
            i = words.index(to_join)
            words = words[:i] + [to_join + ' ' +  words[i+1]] + words[i+2:]
        return words

    def _parse_color_name(self, color_name):
        words = color_name.split(' ')
        try:
            words = self._join_word(words, 'light')
            words = self._join_word(words, 'not')
            code = ''.join(COLOR_CODES[word] for word in words)
        except KeyError, IndexError:
            raise ValueError('%s is not an accepted color.' % color_name)
        return code

    def setLevelColor(self, lvl, color):
        """
        Modify or set the color associated with a log level.

        Args:
            lvl (int): log level to associate a color with.
            color (str): name of the color/style, e.g. 'bold red.'
        """
        self.levelColors[lvl] = color

    def getLevelColor(self, lvl):
        """
        Get the color associated with a log level.

        Args:
            lvl (int): log level.
        """
        return self.levelColors[lvl]

    _re_color = re.compile(r'(\#\(([a-zA-Z][a-zA-Z ]*)\))')

    def format(self, record):
        """
        Format a log message (LogRecord instance).

        Args:
            record: LogRecord instance to format.
        """
        txt = super(ColorFormatter, self).format(record)
        for match in self._re_color.finditer(txt):
            s, color = match.groups()
            if color == 'level':
                color = self.levelColors[record.levelno]
            code = self._parse_color_name(color)
            if not self.additive:
                code = COLOR_CODES['plain'] + code
            # It's a bit  wasteful to parse the color name even if
            # we are ignoring it. The goal is to catch bugs early, i.e.
            # avoid cases were a program runs fine when piped but
            # fails in TTY because of an invalid color name.
            if not IS_TTY:
                code = ""
            txt = txt.replace(s, code, 1)
            if self.autoclear:
                txt += COLOR_CODES['plain']
        return txt


def test():
    handler = logging.StreamHandler()
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    formatter = ColorFormatter()
    handler.setFormatter(formatter)

    logger.debug('#(magenta)this is a magenta debug message')
    logger.info('this is an info message')
    logger.warn('this is a warning message')
    logger.error('this is an error message')
    logger.critical('this is a critical message')

    formatter.setLevelColor(logging.INFO, 'bold inverted cyan')
    logger.info('#(blink)this is a funky info message')


if __name__ == "__main__":
    test()
