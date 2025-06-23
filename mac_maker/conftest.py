"""Pytest fixtures for mac_maker."""
# pylint: disable=redefined-outer-name

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
def global_spec_file_mock(
    global_spec_file_path_mock: str,
    global_spec_mock: Spec,
) -> spec_file.SpecFile:
  spec_file_mock = spec_file.SpecFile()
  spec_file_mock.content = global_spec_mock
  spec_file_mock.path = global_spec_file_path_mock
  return spec_file_mock


@pytest.fixture
def global_spec_file_path_mock() -> str:
  return "/path/to/spec_file.json"
