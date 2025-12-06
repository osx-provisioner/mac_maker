"""Pytest fixtures for mac_maker."""
# pylint: disable=redefined-outer-name

from dataclasses import asdict
from typing import Any, Dict
from unittest import mock

import pytest
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile import precheck, spec_file


@pytest.fixture
def global_git_branch_mock() -> str:
  return "development"


@pytest.fixture
def global_git_url_mock() -> str:
  return "https://github.com/osx-provisioner/mac_maker"


@pytest.fixture
def global_precheck_data_mock() -> precheck.TypePrecheckFileData:
  return precheck.TypePrecheckFileData(
      notes='some notes',
      env='environment test data',
  )


@pytest.fixture
def global_spec_data_mock(global_spec_mock: Spec) -> Dict[str, Any]:
  return asdict(global_spec_mock)


@pytest.fixture
def global_spec_mock() -> Spec:
  return Spec(
      workspace_root_path='/path/to/root',
      profile_data_path='/path/to/profile_data',
      galaxy_requirements_file='/path/to/galaxy_requirements_file',
      playbook='/path/to/playbook',
      roles_path=[
          '/path/to/roles1',
          '/path/to/roles2',
      ],
      collections_path=[
          '/path/to/collections1',
          '/path/to/collections2',
      ],
      inventory="/path/to/inventory"
  )


@pytest.fixture
def global_spec_file_instance() -> spec_file.SpecFile:
  return spec_file.SpecFile()


@pytest.fixture
def global_spec_file_mock(
    # pylint: disable=unused-argument
    global_spec_file_instance: spec_file.SpecFile,
    global_spec_file_reader_mock: mock.Mock,
    global_spec_file_writer_mock: mock.Mock,
) -> spec_file.SpecFile:
  return global_spec_file_instance


@pytest.fixture
def global_spec_file_reader_mock(
    global_spec_file_instance: spec_file.SpecFile,
    global_spec_mock: Spec,
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:

  def mock_data_assignment() -> None:
    global_spec_file_instance.content = global_spec_mock

  instance = mock.Mock(side_effect=mock_data_assignment)
  monkeypatch.setattr(spec_file.SpecFile, "load", instance)
  return instance


@pytest.fixture
def global_spec_file_writer_mock(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(spec_file.SpecFile, "write", instance)
  return instance


@pytest.fixture
def global_spec_file_path_mock() -> str:
  return "/path/to/spec_file.json"
