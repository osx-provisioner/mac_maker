"""Test the ProvisionerJobBase class."""

from typing import Dict
from unittest import mock

import pytest
from mac_maker.__helpers__.parametrize import templated_ids
from mac_maker.config import PRECHECK_SUCCESS_MESSAGE
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.jobs.bases.tests.conftest import ProvisionerMocks
from mac_maker.utilities import precheck, spec


class TestJobsBase:
  """Test the ProvisionerJobBase class."""

  def test_initialize__has_spec_extractor(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
  ) -> None:
    assert isinstance(
        concrete_provisioning_job.jobspec_extractor,
        spec.JobSpecExtractor,
    )

  def test_initialize__has_precheck_extractor(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
  ) -> None:
    assert isinstance(
        concrete_provisioning_job.precheck_extractor,
        precheck.PrecheckExtractor,
    )

  @pytest.mark.parametrize(
      "precheck_args",
      (
          {},
          {
              "notes": True
          },
          {
              "notes": False
          },
      ),
      ids=templated_ids("args:{0}"),
  )
  @pytest.mark.parametrize(
      "validity",
      ("True", "False"),
      ids=templated_ids("validity:{0}", lambda arg: str(arg)[0]),
  )
  def test_precheck__vary_validity__vary_args__instantiates_validator(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      mocked_precheck_config_validator: mock.Mock,
      global_precheck_data_mock: precheck.TypePrecheckFileData,
      precheck_args: Dict[str, bool],
      validity: bool,
  ) -> None:
    mocked_precheck_config_validator.return_value \
        .validate_environment.return_value = {
            'is_valid': validity,
            'violations': [],
        }

    concrete_provisioning_job.precheck(**precheck_args)

    mocked_precheck_config_validator.assert_called_once_with(
        global_precheck_data_mock['env']
    )

  @pytest.mark.parametrize(
      "precheck_args",
      (
          {},
          {
              "notes": True
          },
      ),
      ids=templated_ids("args:{0}"),
  )
  def test_precheck__valid_env__with_notes__calls_echo(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      mocked_click_echo: mock.Mock,
      global_precheck_data_mock: precheck.TypePrecheckFileData,
      mocked_validate_environment: mock.Mock,
      precheck_args: Dict[str, bool],
  ) -> None:
    mocked_validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    concrete_provisioning_job.precheck(**precheck_args)

    assert mocked_click_echo.mock_calls == [
        mock.call(global_precheck_data_mock['notes']),
        mock.call(PRECHECK_SUCCESS_MESSAGE),
    ]

  @pytest.mark.parametrize(
      "precheck_args",
      ({
          "notes": False
      },),
      ids=templated_ids("args:{0}"),
  )
  def test_precheck__valid_env__vary_notes__calls_echo(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      mocked_click_echo: mock.Mock,
      mocked_validate_environment: mock.Mock,
      precheck_args: Dict[str, bool],
  ) -> None:
    mocked_validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    concrete_provisioning_job.precheck(**precheck_args)

    assert mocked_click_echo.mock_calls == [
        mock.call(PRECHECK_SUCCESS_MESSAGE),
    ]

  @pytest.mark.parametrize(
      "precheck_args",
      (
          {},
          {
              "notes": True
          },
          {
              "notes": False
          },
      ),
      ids=templated_ids("args:{0}"),
  )
  def test_precheck__invalid_env__vary_notes__calls_echo(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      mocked_click_echo: mock.Mock,
      mocked_sys: mock.Mock,
      mocked_validate_environment: mock.Mock,
      precheck_args: Dict[str, bool],
  ) -> None:
    mocked_sys.exit.side_effect = SystemExit
    mocked_validate_environment.return_value = {
        'is_valid': False,
        'violations': ['violation1', 'violation2'],
    }

    with pytest.raises(SystemExit):
      concrete_provisioning_job.precheck(**precheck_args)

    assert mocked_click_echo.mock_calls == [
        mock.call(violation)
        for violation in mocked_validate_environment.return_value['violations']
    ]

  def test_provision__creates_inventory_file(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      provisioner_mocks: ProvisionerMocks,
  ) -> None:
    concrete_provisioning_job.provision()

    provisioner_mocks.mocked_inventory_file.assert_called_once_with(
        concrete_provisioning_job.get_state()
    )
    provisioner_mocks.mocked_inventory_file.return_value \
        .write_inventory_file.assert_called_once_with()

  def test_provision__prompts_for_sudo(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      provisioner_mocks: ProvisionerMocks,
  ) -> None:
    concrete_provisioning_job.provision()

    provisioner_mocks.mocked_sudo.assert_called_once_with()
    provisioner_mocks.mocked_sudo.return_value \
        .prompt_for_sudo.assert_called_once_with()

  def test_provision__starts_ansible_runner(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      provisioner_mocks: ProvisionerMocks,
  ) -> None:
    concrete_provisioning_job.provision()

    provisioner_mocks.mocked_ansible_runner.assert_called_once_with(
        concrete_provisioning_job.get_state()
    )
    provisioner_mocks.mocked_ansible_runner.return_value \
        .start.assert_called_once_with()
