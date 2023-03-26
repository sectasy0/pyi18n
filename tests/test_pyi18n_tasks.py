# flake8: noqa
from typing import List
from pytest import raises
from .helpers import test_path, capture, empty_locales
from pyi18n.pyi18n_tasks import cli
from pyi18n.tasks import normalize
from argparse import Namespace
from unittest.mock import patch, MagicMock


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


def test_cli_no_args(capsys):
    with raises(SystemExit):
        cli()
    captured = capsys.readouterr()
    assert 'error: the following arguments are required: normalize\n' in captured.err


def test_cli_with_args():
    args = Namespace(normalize=True, path="test_path")
    with patch('argparse.ArgumentParser.parse_args', return_value=args), \
         patch.object(normalize, 'normalize_locales', MagicMock()) as mock_method:
        cli()
    mock_method.assert_called_once_with("test_path")


def test_cli_without_normalize_flag():
    args = Namespace(normalize=False, path="test_path")
    with patch('argparse.ArgumentParser.parse_args', return_value=args), \
         patch.object(normalize, 'normalize_locales', MagicMock()) as mock_method:
        cli()
    mock_method.assert_not_called()


def test_cli_with_default_path():
    args = Namespace(normalize=True, path="locales")
    with patch('argparse.ArgumentParser.parse_args', return_value=args), \
         patch.object(normalize, 'normalize_locales', MagicMock()) as mock_method:
        cli()
    mock_method.assert_called_once_with("locales")
