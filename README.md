<div align="center">

[![pypi](https://img.shields.io/pypi/v/enum-actions)](https://pypi.org/project/enum-actions/)
[![github](https://img.shields.io/static/v1?label=&message=github&color=grey&logo=github)](https://github.com/aatifsyed/enum-actions)

</div>

# `enum-actions`
For easy selection command-line selection of an `enum.Enum` variant with `argparse.Action`s.

Use it like this:
```python
>>> from enum_actions import enum_action
>>> from argparse import ArgumentParser
>>> import enum

>>> class MyEnum(enum.Enum):
...     A = 1
...     B = 2

>>> parser = ArgumentParser()
>>> _ = parser.add_argument("-e", "--enum", action=enum_action(MyEnum), default="a", help="pick a variant") # create an action for your enum
>>> args = parser.parse_args() # there will be an instance of MyEnum in the args object

```

## Features
### Choices are handled transparently
```text
foo.py --help

usage: foo.py [-h] [-e {a,b}]

optional arguments:
  -h, --help            show this help message and exit
  -e {a,b}, --enum {a,b}
                        pick a variant (default: b)
```

### Defaults are handled transparently
Having a default string or enum will both work
```python
parser.add_argument("--enum", action=enum_action(MyEnum), default="a")
parser.add_argument("--enum", action=enum_action(MyEnum), default=MyEnum.A)
```
