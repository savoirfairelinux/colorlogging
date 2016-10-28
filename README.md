# colorlogging
Simple color logging for Python.

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Example](#example)
* [Colors and Styles](#colors)
* [Options](#options)
* [Todo](#todo)

## Requirements

Python 2.7+ (Python 3 supported).

No additional requirements.

## Installation

This package is not (yet?) on pypi. To install:

```bash
git clone https://github.com/jbchouinard/colorlogging.git
cd colorlogging
pip install .
```

## Example

colorlogging has a single class, ``ColorFormatter``.

```python
import logging
from colorlogging import ColorFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

fmt = "%(asctime)s %(levelname)s: #(magenta)%(message)s"
formatter = ColorFormatter(fmt)
handler.setFormatter(formatter)

logger.info('This will be printed in magenta!')
```
Format strings are handled as usual (see the Formatter documentation,
[py2](https://docs.python.org/2/library/logging.html#formatter-objects),
[py3](https://docs.python.org/3/library/logging.html#formatter-objects)),
with one addition:

Style modifiers like ``#(bold green)``. The format
string in the previous example will print log messages in magenta.

You can also style a message directly:

```python
logger.info('#(underlined green)This will be underlined and green!')
```

We use shell codes to color the output, so using this formatter with anything
but a StreamHandler connected to stdout is not useful or recommended.

We check if stdout is a terminal; if stdout is piped to a file or program, the
color codes will not be printed. Support for stderr should be added in the
future.

## Colors and Styles

The syntax for  modifiers is ``#([style] [color])``,
where ``style`` and ``color`` are one of the following:

| Styles               | Colors          |
|----------------------|-----------------|
| [not] bold           | black           |
| [not] underlined     | white           |
| [not] dim            | [light] gray    |
| [not] blink          | [light] red     |
| [not] inverted       | [light] green   |
| [not] hidden         | [light] yellow  |
| plain                | [light] blue    |
|                      | [light] magenta |
|                      | [light] cyan    |
|                      | level           |
 
Colors and styles can be combined; for example ``bold red``, ``bold light red``,
etc.

``red blue`` will parse fine, but you'll just get blue output.  Unfortunately we
can't do color mixing with shell codes.

``plain`` clears all styles and colors.

``level`` is a special color that depends on the log level of the message.  By
default info is green, warning is yellow, etc.  The most common use case would
be coloring the level name:

```python
fmt = "%(asctime)s #(level)%(levelname)s#(plain): %(message)s"
formatter = ColorFormatter(fmt)
```

Note the usage of ``plain``; without it the message would be colored too.

The defaults can be changed, or new levels added, with the ``setLevelColor``
method:

```python
formatter.setLevelColor(logging.INFO, 'inverted light cyan')
```

## Options

``ColorFormatter``'s behaviour depends on two options:

``additive``: in additive mode, colors and styles are applied cumulatively.
Otherwise, style modifiers clear all previous modifiers. The default is
``False``. Example:

```python
formatter = ColorFormatter(additive=True)
handler.setFormatter(formatter)

logger.info('#(bold)This is bold. #(blue)This is bold and blue. #(not bold)This
is only blue.')

formatter = ColorFormatter()  # additive is False by default
handler.setFormatter(formatter)

logger.info('#(bold)This is bold. #(blue)This is only blue, not bold.')
```

Negative modifiers, e.g. ``#(not bold)`` can be used in additive mode for
complex styling.

Note that the negative modifiers do not work correctly in some terminal
emulators.

```autoclear```: adds ``#(plain)`` at the end of every message. Defaults to
``True``.  If set to ``False`` and ``#(plain)``is omitted, the shell will
continue printing in whatever style was set, past the log line.

## Todo

* Make ColorFormatter useable with stderr (only problem is that the TTY check is
  currently hardcoded to stdout.)
