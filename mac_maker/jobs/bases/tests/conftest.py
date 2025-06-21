"""Pytest fixtures for mac_maker job base classes."""
# pylint: disable=redefined-outer-name

from typing import NamedTuple, Type, cast
from unittest import mock

import pytest
from mac_maker.jobs.bases import provisioner
from mac_maker.utilities import precheck, state


class ProvisionerMocks(NamedTuple):
  mocked_ansible_runner: mock.Mock
  mocked_inventory_file: mock.Mock
  mocked_state: state.TypeState
  mocked_sudo: mock.Mock


@pytest.fixture
def provisioner_mocks(
    global_state_data_mock: state.TypeState,
    mocked_ansible_runner: mock.Mock,
    mocked_inventory_file: mock.Mock,
    mocked_sudo: mock.Mock,
) -> ProvisionerMocks:
  return ProvisionerMocks(
      mocked_ansible_runner=mocked_ansible_runner,
      mocked_inventory_file=mocked_inventory_file,
      mocked_state=global_state_data_mock,
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
def mocked_sudo(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "SUDO",
      instance,
  )
  return instance


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
def mocked_validate_environment(
    mocked_precheck_config_validator: mock.Mock,
) -> mock.Mock:
  return cast(
      mock.Mock,
      mocked_precheck_config_validator.return_value.validate_environment,
  )


@pytest.fixture
def concrete_provisioning_job_class(
    global_precheck_data_mock: precheck.TypePrecheckFileData,
    global_state_data_mock: state.TypeState
) -> Type[provisioner.ProvisionerJobBase]:

  class ConcreteJob(provisioner.ProvisionerJobBase):
    """Concrete test implementation of the ProvisionerJobBase class."""

    def get_precheck_content(self) -> precheck.TypePrecheckFileData:
      return global_precheck_data_mock

    def get_state(self) -> state.TypeState:
      return global_state_data_mock

  return ConcreteJob


@pytest.fixture
def concrete_provisioning_job(
    concrete_provisioning_job_class: Type[provisioner.ProvisionerJobBase],
) -> provisioner.ProvisionerJobBase:
  instance = concrete_provisioning_job_class()
  return instance
