"""Pytest fixtures for the Mac Maker profile spec file."""
# pylint: disable=redefined-outer-name

from typing import Any, Callable, Dict
from unittest import mock

import pytest
from mac_maker.profile import spec_file


@pytest.fixture
def mocked_jsonfile_read() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_jsonfile_write() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_spec_file_validator() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_spec_file_module(
    global_spec_data_mock: Dict[str, Any],
    mocked_jsonfile_read: mock.Mock,
    mocked_jsonfile_write: mock.Mock,
    mocked_spec_file_validator: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        spec_file.JSONFileReader,
        "load_json_file",
        mocked_jsonfile_read,
    )
    monkeypatch.setattr(
        spec_file.JSONFileWriter,
        "write_json_file",
        mocked_jsonfile_write,
    )
    monkeypatch.setattr(
        spec_file,
        "SpecFileValidator",
        mocked_spec_file_validator,
    )

    mocked_jsonfile_read.return_value = global_spec_data_mock

  return setup


@pytest.fixture
def spec_file_instance(
    setup_spec_file_module: Callable[[], None],
) -> spec_file.SpecFile:
  setup_spec_file_module()

  return spec_file.SpecFile()
