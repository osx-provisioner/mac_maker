"""Pytest fixtures for mac_maker job base classes."""
# pylint: disable=redefined-outer-name

from typing import NamedTuple, Type, cast
from unittest import mock

import pytest
from mac_maker.ansible_controller.spec import Spec
from mac_maker.jobs.bases import provisioner
from mac_maker.profile import precheck


class ProvisionerMocks(NamedTuple):
  mocked_ansible_inventory_file: mock.Mock
  mocked_ansible_runner: mock.Mock
  mocked_spec: Spec
  mocked_sudo: mock.Mock


@pytest.fixture
def provisioner_mocks(
    global_spec_mock: Spec,
    mocked_ansible_inventory_file: mock.Mock,
    mocked_ansible_runner: mock.Mock,
    mocked_sudo: mock.Mock,
) -> ProvisionerMocks:
  return ProvisionerMocks(
      mocked_ansible_inventory_file=mocked_ansible_inventory_file,
      mocked_ansible_runner=mocked_ansible_runner,
      mocked_spec=global_spec_mock,
      mocked_sudo=mocked_sudo,
  )


@pytest.fixture
def mocked_ansible_inventory_file(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "AnsibleInventoryFile",
      instance,
  )
  return instance


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
def mocked_precheck_validator(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "PrecheckValidator",
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
    mocked_precheck_validator: mock.Mock,
) -> mock.Mock:
  return cast(
      mock.Mock,
      mocked_precheck_validator.return_value.validate_environment,
  )


@pytest.fixture
def concrete_provisioning_job_class(
    global_precheck_data_mock: precheck.TypePrecheckFileData,
    global_spec_mock: Spec
) -> Type[provisioner.ProvisionerJobBase]:

  class ConcreteJob(provisioner.ProvisionerJobBase):
    """Concrete test implementation of the ProvisionerJobBase class."""

    def get_precheck_content(self) -> precheck.TypePrecheckFileData:
      return global_precheck_data_mock

    def get_spec(self) -> Spec:
      return global_spec_mock

  return ConcreteJob


@pytest.fixture
def concrete_provisioning_job(
    concrete_provisioning_job_class: Type[provisioner.ProvisionerJobBase],
) -> provisioner.ProvisionerJobBase:
  instance = concrete_provisioning_job_class()
  return instance
