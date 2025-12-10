"""Test the Mac Maker CLI."""
from typing import Callable, Tuple, Union
from unittest import mock

import pytest
from mac_maker.__helpers__.parametrize import named_parameters
from mac_maker.tests.conftest import InvokeType


class TestCli:
  """Test the Mac Maker CLI."""

  mocked_folder_path = "/non/existent/folder/path"
  mocked_git_url = "https://github.com/non/existent/.git"
  mocked_git_branch = "develop"
  mocked_spec_file = "/non/existent/spec_file/path"

  @pytest.mark.parametrize(
      "mocked_job,command",
      named_parameters(
          (
              "mocked_job_spec_file",
              f"precheck spec {mocked_spec_file}",
          ),
          (
              "mocked_job_spec_file",
              f"apply spec {mocked_spec_file}",
          ),
          (
              "mocked_job_github",
              f"precheck git {mocked_git_url}",
          ),
          (
              "mocked_job_github",
              f"precheck git {mocked_git_url} --branch {mocked_git_branch}"
          ),
          (
              "mocked_job_github",
              f"apply git {mocked_git_url}",
          ),
          (
              "mocked_job_github",
              f"apply git {mocked_git_url} --branch {mocked_git_branch}"
          ),
          (
              "mocked_job_version",
              "version",
          ),
          names=[1],
      ),
      indirect=["mocked_job"],
  )
  @pytest.mark.parametrize(
      "global_flags", [("debug",), ()], ids=("debug_flag", "no_flags")
  )
  def test_vary_command__configures_logging_correctly(
      self,
      invoke: InvokeType,
      mocked_logger: mock.Mock,
      mocked_job: mock.Mock,  # pylint: disable=unused-argument
      command: str,
      global_flags: Union[Tuple[()], Tuple[str, ...]],
  ) -> None:
    invoke(command, global_flags=global_flags)

    mocked_logger.assert_called_once_with(debug="debug" in global_flags)

  @pytest.mark.parametrize(
      "mocked_job,command",
      named_parameters(
          ("mocked_job_version", "version"),
          names=[1],
      ),
      indirect=["mocked_job"],
  )
  def test_vary_basic_command__invokes_job_correctly(
      self,
      invoke: InvokeType,
      mocked_job: mock.Mock,
      command: str,
  ) -> None:
    invoke(command)

    mocked_job.assert_called_once_with()
    mocked_job.return_value.invoke.assert_called_once_with()

  @pytest.mark.parametrize(
      "mocked_job,command,args",
      named_parameters(
          (
              "mocked_job_folder",
              f"precheck folder {mocked_folder_path}",
              (mocked_folder_path,),
          ),
          (
              "mocked_job_github",
              f"precheck github {mocked_git_url}",
              (mocked_git_url, None),
          ),
          (
              "mocked_job_github",
              f"precheck github {mocked_git_url} --branch {mocked_git_branch}",
              (mocked_git_url, mocked_git_branch),
          ),
          (
              "mocked_job_spec_file",
              f"precheck spec {mocked_spec_file}",
              (mocked_spec_file,),
          ),
          names=[1],
      ),
      indirect=["mocked_job"],
  )
  def test_vary_pre_check_command__paths_exist__invokes_precheck_correctly(
      self,
      invoke: InvokeType,
      mocked_job: mock.Mock,
      setup_click_paths_exist: Callable[[], None],
      command: str,
      args: Tuple[str],
  ) -> None:
    setup_click_paths_exist()

    invoke(command)

    mocked_job.assert_called_once_with(*args)
    mocked_job.return_value.precheck.assert_called_once_with()

  @pytest.mark.parametrize(
      "mocked_job,command",
      named_parameters(
          (
              "mocked_job_folder",
              f"precheck folder {mocked_folder_path}",
          ),
          (
              "mocked_job_spec_file",
              f"precheck spec {mocked_spec_file}",
          ),
          names=[1],
      ),
      indirect=["mocked_job"],
  )
  def test_vary_pre_check_command__paths_do_not_exist__does_not_invoke_precheck(
      self,
      invoke: InvokeType,
      mocked_job: mock.Mock,
      setup_click_do_not_exist: Callable[[], None],
      command: str,
  ) -> None:
    setup_click_do_not_exist()

    invoke(command)

    mocked_job.assert_not_called()
    mocked_job.return_value.precheck.assert_not_called()

  @pytest.mark.parametrize(
      "mocked_job,command,args",
      named_parameters(
          (
              "mocked_job_folder",
              f"apply folder {mocked_folder_path}",
              (mocked_folder_path,),
          ),
          (
              "mocked_job_github",
              f"apply github {mocked_git_url}",
              (mocked_git_url, None),
          ),
          (
              "mocked_job_github",
              f"apply github {mocked_git_url} --branch {mocked_git_branch}",
              (mocked_git_url, mocked_git_branch),
          ),
          (
              "mocked_job_spec_file",
              f"apply spec {mocked_spec_file}",
              (mocked_spec_file,),
          ),
          names=[1],
      ),
      indirect=["mocked_job"],
  )
  def test_vary_apply_command__paths_exist__invokes_provision_correctly(
      self,
      invoke: InvokeType,
      mocked_job: mock.Mock,
      setup_click_paths_exist: Callable[[], None],
      command: str,
      args: Tuple[str],
  ) -> None:
    setup_click_paths_exist()

    invoke(command)

    mocked_job.assert_called_once_with(*args)
    mocked_job.return_value.precheck.assert_called_once_with(notes=False)
    mocked_job.return_value.provision.assert_called_once_with()

  @pytest.mark.parametrize(
      "mocked_job,command",
      named_parameters(
          (
              "mocked_job_folder",
              f"apply folder {mocked_folder_path}",
          ),
          (
              "mocked_job_spec_file",
              f"apply spec {mocked_spec_file}",
          ),
          names=[1],
      ),
      indirect=["mocked_job"],
  )
  def test_vary_apply_command__paths_do_not_exist__invokes_provision_correctly(
      self,
      invoke: InvokeType,
      mocked_job: mock.Mock,
      setup_click_do_not_exist: Callable[[], None],
      command: str,
  ) -> None:
    setup_click_do_not_exist()

    invoke(command)

    mocked_job.assert_not_called()
    mocked_job.return_value.precheck.assert_not_called()
    mocked_job.return_value.provision.assert_not_called()
