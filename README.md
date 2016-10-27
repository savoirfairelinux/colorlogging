# colorlogging
Simple color logging for Python.

## Requirements

Python 2.7+ (Python 3 supported).

No additional requirements.

## Installation

This package is not (yet?) on pypi. To install:

```
git clone https://github.com/jbchouinard/colorlogging.git
cd colorlogging
pip install .
```
or

```
git clone https://github.com/jbchouinard/colorlogging.git
cp -r colorlogging/colorlogging <your project>
```

## Usage

colorlogging has a single class, ColorFormatter.

```
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
```
Format strings are handled as usual (see logging.Formatter documentation), with one addition:

Modifiers like #(\<color name\>) are used to color output. The format string in this example will print log messages
in magenta.

Modifiers can be written directly in messages, for styling particular messages:

```
logger.info('#(underlined green)This message will be underlined and green!')
```

We use shell codes to color the output, so using this formatter with anything but a StreamHandler
connected to a shell is not useful or recommended.

We do check if stdout is a terminal; if stdout is piped to a file or program, the color codes will not be
printed. (Support for stderr should be added in the future.)

## Colors

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
 * [not] bold
 * [not] dim
 * [not] underlined
 * [not] blink
 * [not] inverted
 * [not] hidden
 * plain
 * default
 * normal
 * level
 
Colors and styles can be combined; for example "bold red", "bold light red", etc.

"red blue" will parse fine, but you'll just get blue output. Unfortunately we can't do color mixing with shell codes.

Plain, default and normal all mean the same thing, they are just synonyms for convenience. They clear all styles/colors.

**level** is a special color that depends on the log level of the message. By default info is green, warning is yellow, etc.
The most common use case would be coloring the level name:

```
fmt = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = ColorFormatter(fmt)
```

The defaults can be changed, or new levels added, with ``ColoredFormatter.setLevelColor``:

```
formatter.setLevelColor(logging.INFO, 'cyan')
```

## Options

ColorFormatter's behaviour depends on two options:

``additive``: in additive mode, colors and styles are applied cumulatively. Otherwise, #(\<color name\>) modifiers
clear all previous modifiers. The default is False. Example:

```
formatter = ColorFormatter(additive=True)
handler.setFormatter(formatter)

logger.info('#(bold)This is bold. #(blue)This is bold and blue. #(not bold)This is only blue.')

formatter = ColorFormatter()  # additive is False by default
handler.setFormatter(formatter)

logger.info('#(bold)This is bold. #(blue)This is only blue, not bold.')
```

Negative modifiers, e.g. #(not bold) can be used in additive mode for complex styling.

```autoclear```: Adds #(plain) at the end of every message. Defaults to True. If set to False and #(plain) is omitted,
the shell will continue printing in whatever style was set, past the log message.

## TODO

* Make ColorFormatter useable with stderr (only problem is that the TTY check is currently hardcoded to stdout.)
