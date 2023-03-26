# flake8: noqa
from pyi18n import helpers
from tests.helpers import namespaced_path
import pytest

import yaml, json


def test_get_files_yml():
    files: list = helpers.get_files(f"{namespaced_path}/en_US", 'yml')
    assert files == ['common.yml', 'analysis.yml']


def test_get_files_yml_invalid_namespace():
    files: list = helpers.get_files(f"{namespaced_path}/", 'yml')
    assert not files


def test_get_files_yml_invalid_extension():
    files: list = helpers.get_files(f"{namespaced_path}/de_DE", 'invalid')
    assert not files


def test_get_files_yml_without_extension():
    files: list = helpers.get_files(f"{namespaced_path}/de_DE", '')
    assert not files


def test_get_files_yml_invalid_path():
    with pytest.raises(FileNotFoundError):
        helpers.get_files('invalid_path/de_DE', 'yml')


def test_get_files_yml_without_path():
    with pytest.raises(FileNotFoundError):
        helpers.get_files('', 'yml')


def test_get_files_json():
    files: list = helpers.get_files(f"{namespaced_path}/en_US", 'json')
    assert files == ['common.json', 'analysis.json']


def test_get_files_json_invalid_namespace():
    files: list = helpers.get_files(f"{namespaced_path}/", 'json')
    assert not files


def test_get_files_json_invalid_extension():
    files: list = helpers.get_files(f"{namespaced_path}/de_DE", 'invalid')
    assert not files


def test_get_files_json_without_extension():
    files: list = helpers.get_files(f"{namespaced_path}/de_DE", '')
    assert not files


def test_get_files_json_invalid_path():
    with pytest.raises(FileNotFoundError):
        helpers.get_files('invalid_path/de_DE', 'json')


def test_get_files_json_without_path():
    with pytest.raises(FileNotFoundError):
        helpers.get_files('', 'json')


def test_load_file_yaml():
    file_path: str = f"{namespaced_path}/de_DE/common.yml"
    result: dict = helpers.load_file(file_path, yaml, 'yaml')
    assert isinstance(result, dict)
    assert result == {'farewell': 'Auf Wiedersehen', 'greeting': 'Hallo', 'no': 'Nein', 'yes': 'Ja'}


def test_load_file_yaml_invalid_type():
    file_path: str = f"{namespaced_path}/de_DE/common.yml"
    with pytest.raises(TypeError):
        helpers.load_file(file_path, yaml, 'aaa')


def test_load_file_yaml_without_type():
    file_path: str = f"{namespaced_path}/de_DE/common.yml"
    with pytest.raises(TypeError):
        helpers.load_file(file_path, yaml, None)


def test_load_file_yaml_without_loader():
    file_path: str = f"{namespaced_path}/de_DE/common.yml"
    with pytest.raises(AttributeError):
        helpers.load_file(file_path, None, 'yaml')


def test_load_file_yaml_invalid_loader():
    file_path: str = f"{namespaced_path}/de_DE/common.yml"
    with pytest.raises(AttributeError):
        helpers.load_file(file_path, object, 'yaml')


def test_load_file_yaml_loader_yaml_but_type_json():
    file_path: str = f"{namespaced_path}/de_DE/common.yml"
    with pytest.raises(TypeError):
        helpers.load_file(file_path, yaml, 'json')


# will load json because yaml is a superset of json
def test_load_file_yaml_load_json():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    result: dict = helpers.load_file(file_path, yaml, 'yaml')
    assert isinstance(result, dict)
    assert result == {'farewell': 'Auf Wiedersehen', 'greeting': 'Hallo', 'no': 'Nein', 'yes': 'Ja'}

#####

def test_load_file_json():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    result: dict = helpers.load_file(file_path, json, 'json')
    assert isinstance(result, dict)
    assert result == {'farewell': 'Auf Wiedersehen', 'greeting': 'Hallo', 'no': 'Nein', 'yes': 'Ja'}


# will load because l_type: str, param is for
# yml additional parameters, see pyi18n/helpers.py:76
def test_load_file_json_invalid_type():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    result: dict = helpers.load_file(file_path, json, 'aaa')
    assert isinstance(result, dict)
    assert result == {'farewell': 'Auf Wiedersehen', 'greeting': 'Hallo', 'no': 'Nein', 'yes': 'Ja'}

# like above
def test_load_file_json_without_type():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    result: dict = helpers.load_file(file_path, json, None)
    assert isinstance(result, dict)
    assert result == {'farewell': 'Auf Wiedersehen', 'greeting': 'Hallo', 'no': 'Nein', 'yes': 'Ja'}


def test_load_file_json_without_loader():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    with pytest.raises(AttributeError):
        helpers.load_file(file_path, None, 'json')


def test_load_file_json_invalid_loader():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    with pytest.raises(AttributeError):
        helpers.load_file(file_path, object, 'json')

# works because yaml is a superset of json
# probably redundant test
def test_load_file_json_loader_json_but_type_yaml():
    file_path: str = f"{namespaced_path}/de_DE/common.json"
    result: dict = helpers.load_file(file_path, yaml, 'yaml')
    assert isinstance(result, dict)
    assert result == {'farewell': 'Auf Wiedersehen', 'greeting': 'Hallo', 'no': 'Nein', 'yes': 'Ja'}


def test_load_empty_file_yaml():
    file_path: str = f"{namespaced_path}/de_DE/empty.yaml"
    result: dict = helpers.load_file(file_path, yaml, 'yaml')
    assert result is None


def test_load_empty_file_json():
    file_path: str = f"{namespaced_path}/de_DE/empty.json"
    with pytest.raises(json.decoder.JSONDecodeError):
        helpers.load_file(file_path, json, 'json')
