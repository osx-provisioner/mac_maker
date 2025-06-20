"""Pytest fixtures for mac_maker job base classes."""
# pylint: disable=redefined-outer-name

from typing import NamedTuple, Type, cast
from unittest import mock

import pytest
from mac_maker.utilities import precheck, state
from .. import provisioner


class ProvisionerMocks(NamedTuple):
  mocked_ansible_runner: mock.Mock
  mocked_inventory_file: mock.Mock
  mocked_state: state.TypeState
  mocked_sudo: mock.Mock


@pytest.fixture
def provisioner_mocks(
    mocked_ansible_runner: mock.Mock,
    mocked_inventory_file: mock.Mock,
    mocked_state: state.TypeState,
    mocked_sudo: mock.Mock,
) -> ProvisionerMocks:
  return ProvisionerMocks(
      mocked_ansible_runner=mocked_ansible_runner,
      mocked_inventory_file=mocked_inventory_file,
      mocked_state=mocked_state,
      mocked_sudo=mocked_sudo,
  )


@pytest.fixture
def mocked_ansible_runner(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "AnsibleRunner",
      instance,
  )
  return instance


@pytest.fixture
def mocked_click_echo(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "click",
      mock.Mock(echo=instance),
  )
  return instance


@pytest.fixture
def mocked_inventory_file(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "InventoryFile",
      instance,
  )
  return instance


@pytest.fixture
def mocked_precheck_config_validator(
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "PrecheckConfigValidator",
      instance,
  )
  return instance


@pytest.fixture
def mocked_precheck_data() -> precheck.TypePrecheckFileData:
  return precheck.TypePrecheckFileData(
      notes='some notes',
      env='environment test data',
  )


@pytest.fixture
def mocked_state(
    concrete_provisioning_job: provisioner.ProvisionerJobBase,
    monkeypatch: pytest.MonkeyPatch,
) -> state.TypeState:
  state_instance = cast(
      state.TypeState,
      {'workspace_root_path': '/root/workspace1'},
  )
  monkeypatch.setattr(
      concrete_provisioning_job,
      "mock_state",
      state_instance,
  )
  return state_instance


@pytest.fixture
def mocked_sys(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "sys",
      instance,
  )
  return instance


@pytest.fixture
def mocked_sudo(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "SUDO",
      instance,
  )
  return instance


@pytest.fixture
def mocked_validate_environment(
    mocked_precheck_config_validator: mock.Mock,
) -> mock.Mock:
  return cast(
      mock.Mock,
      mocked_precheck_config_validator.return_value.validate_environment,
  )


@pytest.fixture
def concrete_provisioning_job_class() -> Type[provisioner.ProvisionerJobBase]:

  class ConcreteJob(provisioner.ProvisionerJobBase):
    """Concrete test implementation of the ProvisionerJobBase class."""

    def __init__(self) -> None:
      super().__init__()
      self.mock_precheck_content = cast(precheck.TypePrecheckFileData, {})
      self.mock_state = cast(state.TypeState, {})

    def get_precheck_content(self) -> precheck.TypePrecheckFileData:
      return self.mock_precheck_content

    def get_state(self) -> state.TypeState:
      return self.mock_state

  return ConcreteJob


@pytest.fixture
def concrete_provisioning_job(
    concrete_provisioning_job_class: Type[provisioner.ProvisionerJobBase],
    mocked_precheck_data: precheck.TypePrecheckFileData,
) -> provisioner.ProvisionerJobBase:
  instance = concrete_provisioning_job_class()
  setattr(instance, "mock_precheck_content", mocked_precheck_data)
  return instance
