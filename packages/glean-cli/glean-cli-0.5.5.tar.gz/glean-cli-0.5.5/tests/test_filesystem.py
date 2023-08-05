import pytest

from click.exceptions import ClickException

from glean.filesystem import build_spec_from_local
from tests.helpers import get_fixture_path


@pytest.fixture
def clear_env(monkeypatch: pytest.MonkeyPatch):
    """Don't let actual env vars affect these tests"""
    monkeypatch.delenv("A_NAME", raising=False)


def test_environment_variable_substitution(clear_env, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("A_NAME", "substitution")

    PATH = "model_config_files/with_env_vars"

    build_spec = build_spec_from_local(get_fixture_path(PATH), "")
    assert len(build_spec["inlineConfigFiles"]) == 1

    config_file_details = build_spec["inlineConfigFiles"][0]

    assert config_file_details["fileContents"] == 'glean: "1.0"\nname: substitution\n'
    assert config_file_details["filename"] == "file1.yml"
    assert config_file_details["parentDirectory"].startswith("/tmp/repos")
    assert config_file_details["parentDirectory"].endswith(PATH)


def test_environment_variable_missing(clear_env, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SOMETHING_ELSE", "substitution")

    try:
        build_spec_from_local(get_fixture_path("model_config_files/with_env_vars"), "")
        assert False, "Expected exception to be thrown"
    except ClickException as e:
        assert (
            str(e)
            == "No value found for environment variable substitution in file1.yml: 'A_NAME'"
        )


def test_file_validation():
    with pytest.raises(ClickException) as exception_info: 
        build_spec_from_local(
            get_fixture_path("model_config_files/with_invalid_files"), ""
        )
    assert "Could not parse file" in exception_info.value.args[0]
