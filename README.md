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
import colorlogging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

format = "%(asctime)s %(levelname)s: #(magenta)%(message)s#(plain)"
formatter = colorlogging.ColorFormatter(format)
handler.setFormatter(formatter)

logger.info('This will be printed in magenta!')
logger.info('#(green)This message will be printed in green!')
```
The format string is handled as usual (see logging.Formatter documentation), with one addition:

The modifier #(\<color name\>) is used to start coloring the output. The format string in this example will color
the log message magenta.

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
 
Some of these can be combined, for example "bold red", "bold light red", etc. "red blue" will work but will result in blue output.

Plain, default and normal all mean the same things, they are just synonyms for convenience.

**level** is a special color that depends on the log level of the message. By default info is green, warning is yellow, etc.
The most common use case would be coloring the level name.

The defaults can be changed, or new levels added, with ``ColoredFormatter.setLevelColor``:

```
format = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = colorlogging.ColorFormatter()
formatter.setLevelColor(logging.INFO, 'magenta')
handler.setFormatter(formatter)
```

# Options

ColorFormatter has two options that modify its behaviour.

``additive``: in additive mode, colors and styles are applied cumulatively. Otherwise, #(<color name>) modifiers clear all previous
modifiers. The default is False. Example:

```
formatter = ColorFormatter(additive=True)
handler.setFormatter(formatter)

logger.info('#(bold)This is bold. #(blue)This is bold and blue. #(not bold)This is only blue.')

formatter = ColorFormatter()  # additive is False by default
handler.setFormatter(formatter)

logger.info('#(bold)This is bold. #(blue)This is only blue, not bold.')
```

```autoclear```: True by default. Adds #(plain) at the end of every message. If set to False and #(plain) is omitted,
the shell will continue printing in whatever style was set, past the log message.
