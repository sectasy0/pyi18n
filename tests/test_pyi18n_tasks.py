from typing import List
from pytest import raises
from .helpers import test_path, capture, empty_locales
from pyi18n.pyi18n_tasks import cli

# hack to get percents in test output
def test_cli() -> None:
    with raises(SystemExit):
        cli()


def test_cli_no_params() -> None:
    command: List[str] = ["pyi18n-tasks"]
    out, err, returncode = capture(command)
    assert returncode == 2
    assert out == b""
    assert "usage: pyi18n-tasks" in err.decode("utf-8")


def test_cli_normalize_default_path_not_exists() -> None:
    command: List[str] = ["pyi18n-tasks", "normalize"]
    out, err, returncode = capture(command)
    assert returncode == 1
    assert "does not exist" in out.decode("utf-8")
    assert err == b""


def test_cli_normalize_with_path() -> None:
    command: List[str] = ["pyi18n-tasks", "normalize", "-p", test_path]
    out, err, returncode = capture(command)
    assert returncode == 0
    assert out == b""
    assert err == b""


def test_cli_normalize_with_invalid_path() -> None:
    command: List[str] = ["pyi18n-tasks", "normalize", "-p", "invalid"]
    out, err, returncode = capture(command)
    assert returncode == 1
    assert "does not exist" in out.decode("utf-8")
    assert err == b""


def test_cli_normalize_empty_path() -> None:
    command: List[str] = ["pyi18n-tasks", "normalize", "-p", empty_locales]
    out, err, returncode = capture(command)
    assert returncode == 1
    assert "is empty" in out.decode("utf-8")
    assert err == b""