# colorlogging
Simple color logging for Python.

## Installation

```
git clone https://github.com/jbchouinard/colorlogging.git
cd colorlogging
pip install .
```

Or copy colorlogging/colorlogging to your project if you don't want to install this system-wide.

## Usage

This module has a single class, ColorFormatter.

```
import logging
import colorlogging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)

format = "%(asctime)s %(levelname)s: #(magenta)%(message)s#(plain)"
formatter = colorlogging.ColorFormatter()
handler.setFormatter(formatter)


logger.info('This will be printed in magenta!')
```

The special form #(\<color name\>) is used to start coloring the output. The format string in this example will color
the log message magenta.

For now the only way to stop coloring the output is #(plain). If you don't put #(plain) at the end of the format
the console output will continue printing in magenta forever.

\<color name\> can be one or more of the following colors or styles:
 * black
 * white
 * [light] gray
 * [light] red
 * [light] green
 * [light] yellow
 * [light] blue
 * [light] magenta
 * [light] cyan
 * bold
 * dim
 * underlined
 * blink
 * inverted
 * hidden
 * plain
 * level
 
Some of these can be combined, for example "bold red", "bold light red", etc. "red blue" will work but will result in blue output.

**level** is a special color that depends on the log level of the message. By default info is green, warning is yellow, etc.
The most common use case would be coloring the level name.

The defaults can be changed by ColoredFormatter.setLevelColor:

```
format = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = colorlogging.ColorFormatter()
formatter.setLevelColor(logging.INFO, 'magenta')
handler.setFormatter(formatter)
```

Colors can also be used in log messages:

```
logger.info('#(green)This message will be printed in green!#(plain)')
```

## TODO

* check if stdout is a TTY, if not don't print color codes
* get rid of #(plain), there has to be a better way to do this
