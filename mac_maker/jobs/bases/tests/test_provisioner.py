"""Test the ProvisionerJobBase class."""

from typing import Dict
from unittest import mock

import pytest
from mac_maker.__helpers__.parametrize import templated_ids
from mac_maker.ansible_controller import spec
from mac_maker.config import PRECHECK_SUCCESS_MESSAGE
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.jobs.bases.tests.conftest import ProvisionerMocks
from mac_maker.profile.precheck import TypePrecheckFileData, precheck_extractor
from mac_maker.profile.spec_file import SpecFile


class TestJobsBase:
  """Test the ProvisionerJobBase class."""

  def test_initialize__has_spec_extractor(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
  ) -> None:
    assert isinstance(
        concrete_provisioning_job.spec_file,
        SpecFile,
    )

  def test_initialize__has_precheck_extractor(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
  ) -> None:
    assert isinstance(
        concrete_provisioning_job.precheck_extractor,
        precheck_extractor.PrecheckExtractor,
    )

  def test_get_precheck_content__no_spec_file__initializes_spec_file_once(
      self,
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
      mocked_initialize_spec_file: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job_with_mocked_extractor.spec_file._content = \
        None

    concrete_provisioning_job_with_mocked_extractor.get_precheck_content()
    concrete_provisioning_job_with_mocked_extractor.get_precheck_content()

    mocked_initialize_spec_file.assert_called_once_with()

  def test_get_precheck_content__spec_file__does_not_initialize_spec_file(
      self,
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
      global_spec_mock: spec.Spec,
      mocked_initialize_spec_file: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job_with_mocked_extractor.spec_file._content = \
        global_spec_mock

    concrete_provisioning_job_with_mocked_extractor.get_precheck_content()

    mocked_initialize_spec_file.assert_not_called()

  @pytest.mark.parametrize(
      "initialized",
      ("True", "False"),
      ids=templated_ids("initialized:{0}", lambda arg: str(arg)[0]),
  )
  def test_get_precheck_content__vary_spec_file__returns_correct_value(
      self,
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
      global_spec_mock: spec.Spec,
      global_precheck_data_mock: TypePrecheckFileData,
      initialized: bool,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job_with_mocked_extractor.spec_file._content = (
        global_spec_mock if initialized else None
    )

    results = \
        concrete_provisioning_job_with_mocked_extractor.get_precheck_content()

    assert results == global_precheck_data_mock

  def test_get_spec__no_spec_file__initializes_spec_file_once(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      mocked_initialize_spec_file: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job.spec_file._content = None

    concrete_provisioning_job.get_spec()
    concrete_provisioning_job.get_spec()

    mocked_initialize_spec_file.assert_called_once_with()

  def test_get_spec__spec_file__does_not_initialize_spec_file(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      global_spec_mock: spec.Spec,
      mocked_initialize_spec_file: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job.spec_file._content = global_spec_mock

    concrete_provisioning_job.get_spec()

    mocked_initialize_spec_file.assert_not_called()

  @pytest.mark.parametrize(
      "initialized",
      ("True", "False"),
      ids=templated_ids("initialized:{0}", lambda arg: str(arg)[0]),
  )
  def test_get_spec__vary_spec_file__returns_correct_value(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      global_spec_mock: spec.Spec,
      initialized: bool,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job.spec_file._content = (
        global_spec_mock if initialized else None
    )

    results = concrete_provisioning_job.get_spec()

    assert results == concrete_provisioning_job.spec_file.content

  @pytest.mark.parametrize(
      "initialized",
      ("True", "False"),
      ids=templated_ids("initialized:{0}", lambda arg: str(arg)[0]),
  )
  def test_get_spec__vary_spec_file__calls_echo_correctly(
      self,
      concrete_provisioning_job: ProvisionerJobBase,
      global_spec_mock: spec.Spec,
      initialized: bool,
      mocked_click_echo: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    concrete_provisioning_job.spec_file._content = (
        global_spec_mock if initialized else None
    )

    concrete_provisioning_job.get_spec()

    assert mocked_click_echo.mock_calls == [
        mock.call(concrete_provisioning_job.Messages.spec_file_loaded),
        mock.call(concrete_provisioning_job.spec_file.path),
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
  @pytest.mark.parametrize(
      "validity",
      ("True", "False"),
      ids=templated_ids("validity:{0}", lambda arg: str(arg)[0]),
  )
  def test_precheck__vary_validity__vary_args__instantiates_validator(
      self,
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
      mocked_precheck_validator: mock.Mock,
      global_precheck_data_mock: precheck_extractor.TypePrecheckFileData,
      precheck_args: Dict[str, bool],
      validity: bool,
  ) -> None:
    mocked_precheck_validator.return_value \
        .validate_environment.return_value = {
            'is_valid': validity,
            'violations': [],
        }

    concrete_provisioning_job_with_mocked_extractor.precheck(**precheck_args)

    mocked_precheck_validator.assert_called_once_with(
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
  def test_precheck__valid_env__with_notes__calls_echo_correctly(
      self,
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
      mocked_click_echo: mock.Mock,
      global_precheck_data_mock: precheck_extractor.TypePrecheckFileData,
      mocked_validate_environment: mock.Mock,
      precheck_args: Dict[str, bool],
  ) -> None:
    mocked_validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    concrete_provisioning_job_with_mocked_extractor.precheck(**precheck_args)

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
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
      mocked_click_echo: mock.Mock,
      mocked_validate_environment: mock.Mock,
      precheck_args: Dict[str, bool],
  ) -> None:
    mocked_validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    concrete_provisioning_job_with_mocked_extractor.precheck(**precheck_args)

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
      concrete_provisioning_job_with_mocked_extractor: ProvisionerJobBase,
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
      concrete_provisioning_job_with_mocked_extractor.precheck(**precheck_args)

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

    provisioner_mocks.mocked_ansible_inventory_file.assert_called_once_with(
        concrete_provisioning_job.get_spec()
    )
    provisioner_mocks.mocked_ansible_inventory_file.return_value \
        .write.assert_called_once_with()

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
        concrete_provisioning_job.get_spec()
    )
    provisioner_mocks.mocked_ansible_runner.return_value \
        .start.assert_called_once_with()
