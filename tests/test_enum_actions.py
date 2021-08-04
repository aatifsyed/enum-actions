import pytest
import logging
import enum_actions as subject
import argparse
from pathlib import Path
import enum

logger = logging.getLogger(__name__)


class MyEnum(enum.Enum):
    A = 1
    B = 2


def test_default_str_to_enum():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enum", action=subject.enum_action(MyEnum), default="a")
    args = parser.parse_args([])
    assert isinstance(args.enum, MyEnum)
    assert args.enum == MyEnum.A


def test_default_is_enum():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enum", action=subject.enum_action(MyEnum), default=MyEnum.A)
    args = parser.parse_args([])
    assert isinstance(args.enum, MyEnum)
    assert args.enum == MyEnum.A


@pytest.fixture
def tmp_file(tmp_path: Path):
    tmp_path = tmp_path / "capture.txt"
    return tmp_path


def test_choices(tmp_file: Path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--enum", action=subject.enum_action(MyEnum))

    with open(tmp_file, "w+") as p:
        parser.print_usage(p)
    usage = tmp_file.read_text()
    logger.info(f"{usage=}")
    assert r"{a,b}" in usage


def test_user_selected():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enum", action=subject.enum_action(MyEnum), default=MyEnum.A)
    args = parser.parse_args(["--enum", "b"])
    assert args.enum == MyEnum.B
