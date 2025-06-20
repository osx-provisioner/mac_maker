"""Pytest fixtures for mac_maker."""
# pylint: disable=redefined-outer-name

import pytest
from mac_maker.utilities import precheck, state


@pytest.fixture
def global_precheck_data_mock() -> precheck.TypePrecheckFileData:
  return precheck.TypePrecheckFileData(
      notes='some notes',
      env='environment test data',
  )


@pytest.fixture
def global_state_data_mock() -> state.TypeState:
  return state.TypeState(
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
