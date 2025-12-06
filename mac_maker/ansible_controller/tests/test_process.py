"""Test the AnsibleProcess class."""

import logging
import os
import sys
from logging import Logger
from unittest import mock

import pytest
from mac_maker.__helpers__.logs import decode_logs
from mac_maker.ansible_controller import process
from mac_maker.profile import Profile
from mac_maker.utilities import state

PROCESS_MODULE = process.__name__


class TestAnsibleProcess:
  """Test AnsibleProcess class."""

  def test_init__attributes(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_profile: Profile,
      mocked_state: state.State,
  ) -> None:
    assert ansible_process.error_exit_code == 127
    assert isinstance(ansible_process.log, Logger)
    assert ansible_process.state == mocked_state.state_generate(mocked_profile)

  @pytest.mark.parametrize("m_return_code", [0, 1])
  def test_spawn__not_frozen__vary_return_code__calls_subprocess(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_command: str,
      mocked_popen: mock.Mock,
      mocked_popen_process: mock.Mock,
      m_return_code: int,
  ) -> None:
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = m_return_code

    try:
      ansible_process.spawn(mocked_command)
    except ChildProcessError:
      pass

    mocked_popen.assert_called_once_with(mocked_command, shell=True)
    mocked_popen_process.__enter__.return_value.wait.assert_called_once_with()

  @pytest.mark.parametrize("m_return_code", [0, 1])
  def test_spawn__frozen__vary_return_code__calls_subprocess_with_bundle_path(
      # pylint: disable=too-many-arguments
      self,
      ansible_process_frozen: process.AnsibleProcess,
      mocked_command: str,
      mocked_bundle_path: str,
      mocked_popen: mock.Mock,
      mocked_popen_process: mock.Mock,
      m_return_code: int,
  ) -> None:
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = m_return_code

    try:
      ansible_process_frozen.spawn(mocked_command)
    except ChildProcessError:
      pass

    mocked_popen.assert_called_once_with(
        (
            f'{sys.executable} '
            f'{os.path.join(mocked_bundle_path, "bin", mocked_command)}'
        ),
        shell=True,
    )
    mocked_popen_process.__enter__.return_value.wait.assert_called_once_with()

  @pytest.mark.parametrize("m_return_code", [0, 1])
  def test_spawn__vary_return_code__changes_directory(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_command: str,
      mocked_os_chdir: mock.Mock,
      mocked_popen_process: mock.Mock,
      m_return_code: int,
  ) -> None:
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = m_return_code

    try:
      ansible_process.spawn(mocked_command)
    except ChildProcessError:
      pass

    mocked_os_chdir.assert_called_once_with(
        ansible_process.state['profile_data_path']
    )

  @pytest.mark.parametrize("m_return_code", [0, 1])
  def test_spawn__vary_return_code__sets_environment(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_command: str,
      mocked_ansible_environment: mock.Mock,
      mocked_popen_process: mock.Mock,
      m_return_code: int,
  ) -> None:
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = m_return_code

    try:
      ansible_process.spawn(mocked_command)
    except ChildProcessError:
      pass

    mocked_ansible_environment.assert_called_once_with(ansible_process.state)
    mocked_ansible_environment.return_value.setup.assert_called_once_with()

  def test_spawn__fail__raises_exception(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_command: str,
      mocked_popen_process: mock.Mock,
  ) -> None:
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = 127

    with pytest.raises(ChildProcessError):
      ansible_process.spawn(mocked_command)

  def test_spawn__success__correct_logging(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_command: str,
      mocked_popen_process: mock.Mock,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = 0

    ansible_process.spawn(mocked_command)

    assert decode_logs(caplog.records) == [
        (
            "DEBUG:mac_maker:AnsibleProcess: "
            "Preparing to launch Ansible Process."
        ),
        ("DEBUG:mac_maker:AnsibleProcess: "
         f"Executing '{mocked_command}'"),
        ("DEBUG:mac_maker:AnsibleProcess: "
         f"Spawned worker process {999}"),
        ("DEBUG:mac_maker:AnsibleProcess: "
         "Command completed successfully!"),
    ]

  def test_spawn__fail__correct_logging(
      self,
      ansible_process: process.AnsibleProcess,
      mocked_command: str,
      mocked_popen_process: mock.Mock,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)
    mocked_popen_process.__enter__.return_value.pid = 999
    mocked_popen_process.__enter__.return_value.returncode = 127

    with pytest.raises(ChildProcessError):
      ansible_process.spawn(mocked_command)

    assert decode_logs(caplog.records) == [
        (
            "DEBUG:mac_maker:AnsibleProcess: "
            "Preparing to launch Ansible Process."
        ),
        ("DEBUG:mac_maker:AnsibleProcess: "
         f"Executing '{mocked_command}'"),
        ("DEBUG:mac_maker:AnsibleProcess: "
         f"Spawned worker process {999}"),
        ("ERROR:mac_maker:AnsibleProcess: "
         "Command failed to execute!"),
    ]
