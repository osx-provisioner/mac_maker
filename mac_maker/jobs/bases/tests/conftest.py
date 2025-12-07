"""Pytest fixtures for mac_maker job base classes."""
# pylint: disable=redefined-outer-name

from typing import Callable, NamedTuple, Type, cast
from unittest import mock

import pytest
from mac_maker.ansible_controller import spec
from mac_maker.jobs.bases import provisioner
from mac_maker.profile import precheck, spec_file


class ProvisionerMocks(NamedTuple):
  mocked_ansible_inventory_file: mock.Mock
  mocked_ansible_runner: mock.Mock
  mocked_spec: spec_file.SpecFile
  mocked_sudo: mock.Mock


@pytest.fixture
def provisioner_mocks(
    global_spec_file_instance: spec_file.SpecFile,
    mocked_ansible_inventory_file: mock.Mock,
    mocked_ansible_runner: mock.Mock,
    mocked_sudo: mock.Mock,
) -> ProvisionerMocks:
  return ProvisionerMocks(
      mocked_ansible_inventory_file=mocked_ansible_inventory_file,
      mocked_ansible_runner=mocked_ansible_runner,
      mocked_spec=global_spec_file_instance,
      mocked_sudo=mocked_sudo,
  )


@pytest.fixture
def mocked_ansible_inventory_file() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_ansible_runner() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_click_echo() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_initialize_spec_file() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_precheck_extractor(
    global_precheck_data_mock: precheck.TypePrecheckFileData,
) -> mock.Mock:
  instance = mock.Mock()
  instance.return_value.get_precheck_data.return_value = \
      global_precheck_data_mock
  return instance


@pytest.fixture
def mocked_precheck_validator() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_spec_file(
    global_spec_mock: spec.Spec,
    global_spec_file_instance: spec_file.SpecFile,
    global_spec_file_path_mock: str,
) -> spec_file.SpecFile:
  global_spec_file_instance.content = global_spec_mock
  global_spec_file_instance.path = global_spec_file_path_mock
  return global_spec_file_instance


@pytest.fixture
def mocked_sudo() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_sys() -> mock.Mock:
  instance = mock.Mock()
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
def setup_provisioner_ansible_mocks(
    mocked_ansible_inventory_file: mock.Mock,
    mocked_ansible_runner: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        provisioner,
        "AnsibleInventoryFile",
        mocked_ansible_inventory_file,
    )
    monkeypatch.setattr(
        provisioner,
        "AnsibleRunner",
        mocked_ansible_runner,
    )

  return setup


@pytest.fixture
def setup_provisioner_module(
    mocked_click_echo: mock.Mock,
    mocked_precheck_validator: mock.Mock,
    mocked_sudo: mock.Mock,
    mocked_sys: mock.Mock,
    setup_provisioner_ansible_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    setup_provisioner_ansible_mocks()

    monkeypatch.setattr(
        provisioner,
        "click",
        mock.Mock(echo=mocked_click_echo),
    )
    monkeypatch.setattr(
        provisioner,
        "PrecheckValidator",
        mocked_precheck_validator,
    )
    monkeypatch.setattr(
        provisioner,
        "SUDO",
        mocked_sudo,
    )
    monkeypatch.setattr(
        provisioner,
        "sys",
        mocked_sys,
    )

  return setup


@pytest.fixture
def concrete_provisioning_job_class(
    global_spec_mock: spec.Spec,
    mocked_initialize_spec_file: mock.Mock,
    setup_provisioner_module: Callable[[], None],
) -> Type[provisioner.ProvisionerJobBase]:
  setup_provisioner_module()

  class ConcreteJob(provisioner.ProvisionerJobBase):
    """Concrete test implementation of the ProvisionerJobBase class."""

    def initialize_spec_file(self) -> None:
      self.spec_file.content = global_spec_mock
      mocked_initialize_spec_file()

  return ConcreteJob


@pytest.fixture
def concrete_provisioning_job(
    concrete_provisioning_job_class: Type[provisioner.ProvisionerJobBase],
    mocked_spec_file: spec_file.SpecFile
) -> provisioner.ProvisionerJobBase:
  instance = concrete_provisioning_job_class()
  instance.spec_file = mocked_spec_file
  return instance


@pytest.fixture
def concrete_provisioning_job_with_mocked_extractor(
    concrete_provisioning_job_class: Type[provisioner.ProvisionerJobBase],
    mocked_precheck_extractor: mock.Mock,
    mocked_spec_file: spec_file.SpecFile,
    monkeypatch: pytest.MonkeyPatch,
) -> provisioner.ProvisionerJobBase:
  monkeypatch.setattr(
      provisioner,
      "PrecheckExtractor",
      mocked_precheck_extractor,
  )

  instance = concrete_provisioning_job_class()
  instance.spec_file = mocked_spec_file

  return instance
