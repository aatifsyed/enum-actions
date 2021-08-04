import argparse
import enum
from typing import Any, Callable, Iterable, Optional, Sequence, Tuple, TypeVar, Union

E = TypeVar("E", bound=enum.Enum)

__all__ = ["enum_action"]


def enum_action(enum_class: E):
    """Return an Action which will select a variant of `enum_class` according to the argument.

    `default` may be a str, or an instance of enum_class - the resulting argparse.Namespace will always be an instance of enum_class.

    Note that variants of `enum_class` are expected to have upper case names by this action."""

    class EnumAction(argparse.Action):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            nargs: Optional[Union[int, str]] = None,
            const: Optional[E] = None,
            default: Union[E, str, None] = None,
            type: Optional[
                Union[
                    Callable[[str], E],
                    Callable[[str], E],
                    argparse.FileType,
                ]
            ] = None,
            choices: Optional[Iterable[E]] = None,
            required: bool = False,
            help: Optional[str] = None,
            metavar: Optional[Union[str, Tuple[str, ...]]] = None,
        ) -> None:
            if isinstance(default, str):
                default = enum_class[default.upper()]
            if default is not None:
                if help is None:
                    help = f"(default: {default.name.lower()})"
                else:
                    help = f"{help} (default: {default.name.lower()})"
            self.cls = enum_class
            super().__init__(
                option_strings,
                dest,
                nargs=nargs,
                const=const,
                default=default,
                type=type,
                choices=[variant.name.lower() for variant in enum_class],  # type: ignore
                required=required,
                help=help,
                metavar=metavar,
            )

        def __call__(  # type: ignore
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[str, Sequence[Any], None] = None,
            option_string: Optional[str] = None,
        ) -> None:
            if not isinstance(values, str):
                raise TypeError
            setattr(namespace, self.dest, getattr(self.cls, values.upper()))

    return EnumAction
