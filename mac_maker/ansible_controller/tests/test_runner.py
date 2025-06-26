"""Test the AnsibleRunner class."""

import logging
from typing import Dict, List
from unittest import mock

import pytest
from mac_maker import config
from mac_maker.__helpers__.logs import decode_logs
from mac_maker.ansible_controller import process, runner
from mac_maker.utilities import filesystem, state

RUNNER_MODULE = runner.__name__


class TestAnsibleRunnerClass:
  """Test the AnsibleRunner class."""

  def create_commands(
      self,
      file_system: filesystem.FileSystem,
      debug: bool,
  ) -> List[str]:
    requirements_file_path = \
      file_system.get_galaxy_requirements_file().resolve()
    roles_file_path = file_system.get_roles_path().resolve()
    collections_file_path = file_system.get_collections_path().resolve()
    playbook_file = file_system.get_playbook_file().resolve()
    inventory_file = file_system.get_inventory_file()

    debug_flag = " -vvvv" if debug else ""

    return [
        (
            "ansible-galaxy role install -r"
            f" {requirements_file_path}"
            f" -p {roles_file_path}"
        ),
        (
            "ansible-galaxy collection install -r"
            f" {requirements_file_path}"
            f" -p {collections_file_path}"
        ),
        (
            "ansible-playbook"
            f" {playbook_file}"
            f" -i {inventory_file}"
            " -e "
            "\"ansible_become_password="
            "'{{ lookup('env', 'ANSIBLE_BECOME_PASSWORD') }}'\""
            f"{debug_flag}"
        ),
    ]

  def create_logging_messages(
      self,
      file_system: filesystem.FileSystem,
  ) -> List[str]:
    requirements_file_path = \
      file_system.get_galaxy_requirements_file().resolve()
    roles_file_path = file_system.get_roles_path().resolve()
    collections_file_path = file_system.get_collections_path().resolve()

    return [
        (
            'DEBUG:mac_maker:AnsibleRunner: Reading Profile role '
            'requirements from: ' + str(requirements_file_path)
        ),
        (
            'DEBUG:mac_maker:AnsibleRunner: Reading Profile collection '
            'requirements from: ' + str(requirements_file_path)
        ),
        (
            'DEBUG:mac_maker:AnsibleRunner: Profile Ansible Galaxy roles '
            'have been installed to: ' + str(roles_file_path)
        ),
        (
            'DEBUG:mac_maker:AnsibleRunner: Profile Ansible Galaxy collections '
            'have been installed to: ' + str(collections_file_path)
        ),
        'DEBUG:mac_maker:AnsibleRunner: Invoking Ansible ...',
        'DEBUG:mac_maker:AnsibleRunner: Ansible Playbook has finished!',
    ]

  @pytest.mark.parametrize(
      "kwargs,expected_debug", [
          ({
              "debug": True
          }, True),
          ({
              "debug": False
          }, False),
          ({}, False),
      ]
  )
  def test_init__attributes(
      self,
      mocked_filesystem: filesystem.FileSystem,
      mocked_state: state.State,
      kwargs: Dict[str, bool],
      expected_debug: bool,
  ) -> None:

    instance = runner.AnsibleRunner(
        mocked_state.state_generate(mocked_filesystem),
        **kwargs,
    )

    assert isinstance(instance.log, logging.Logger)
    assert instance.state == mocked_state.state_generate(mocked_filesystem)
    assert instance.debug == expected_debug
    assert isinstance(instance.process, process.AnsibleProcess)

  def test_init__ansible_process(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_filesystem: filesystem.FileSystem,
      mocked_state: state.State,
      mocked_ansible_process: mock.Mock,
  ) -> None:
    mocked_ansible_process.assert_called_with(
        mocked_state.state_generate(mocked_filesystem)
    )
    assert ansible_runner.process == mocked_ansible_process.return_value

  @pytest.mark.parametrize("debug", (True, False))
  def test_start__vary_debug__all_processes_succeed__calls_spawn(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      debug: bool,
  ) -> None:
    ansible_runner.debug = debug
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        None,
        ChildProcessError,
    )

    ansible_runner.start()

    assert mocked_ansible_process.return_value.spawn.call_args_list == [
        mock.call(command)
        for command in self.create_commands(mocked_filesystem, debug)
    ]

  def test_start__all_processes_succeed__correct_logging(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_filesystem: filesystem.FileSystem,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    ansible_runner.start()

    assert decode_logs(caplog.records) == \
        self.create_logging_messages(mocked_filesystem)

  def test_start__all_process_succeed__click_echo(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_click_echo: mock.Mock,
  ) -> None:
    ansible_runner.start()

    assert mocked_click_echo.call_args_list == [
        mock.call(config.ANSIBLE_ROLES_MESSAGE),
        mock.call(config.ANSIBLE_COLLECTIONS_MESSAGE),
        mock.call(config.ANSIBLE_INVOKE_MESSAGE),
    ]

  @pytest.mark.parametrize("debug", (True, False))
  def test_start__vary_debug__first_process_fails__calls_spawn(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      debug: bool,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (ChildProcessError,)

    ansible_runner.start()

    assert mocked_ansible_process.return_value.spawn.call_args_list == [
        mock.call(command)
        for command in self.create_commands(mocked_filesystem, debug)[0:1]
    ]

  def test_start__first_process_fails__click_echo(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_click_echo: mock.Mock,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (ChildProcessError,)
    ansible_runner.start()

    assert mocked_click_echo.call_args_list == [
        mock.call(config.ANSIBLE_ROLES_MESSAGE),
    ]

  def test_start__first_process_fails__logging(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (ChildProcessError,)
    caplog.set_level(logging.DEBUG)

    ansible_runner.start()

    assert decode_logs(caplog.records) == \
        self.create_logging_messages(mocked_filesystem)[0:2]

  @pytest.mark.parametrize("debug", (True, False))
  def test_spawn__vary_debug__second_process_fails__calls_spawn(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      debug: bool,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        ChildProcessError,
    )

    ansible_runner.start()

    assert mocked_ansible_process.return_value.spawn.call_args_list == [
        mock.call(command)
        for command in self.create_commands(mocked_filesystem, debug)[0:2]
    ]

  def test_spawn__second_process_fails__click_echo(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_click_echo: mock.Mock,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        ChildProcessError,
    )
    ansible_runner.start()

    assert mocked_click_echo.call_args_list == [
        mock.call(config.ANSIBLE_ROLES_MESSAGE),
        mock.call(config.ANSIBLE_COLLECTIONS_MESSAGE),
    ]

  def test_spawn__second_process_fails__logging(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        ChildProcessError,
    )
    caplog.set_level(logging.DEBUG)

    ansible_runner.start()

    assert decode_logs(caplog.records) == \
        self.create_logging_messages(mocked_filesystem)[0:3]

  @pytest.mark.parametrize("debug", (True, False))
  def test_spawn__vary_debug__third_process_fails__calls_spawn(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      debug: bool,
  ) -> None:
    ansible_runner.debug = debug
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        None,
        ChildProcessError,
    )

    ansible_runner.start()

    assert mocked_ansible_process.return_value.spawn.call_args_list == [
        mock.call(command)
        for command in self.create_commands(mocked_filesystem, debug)
    ]

  def test_spawn__third_process_fails__click_echo(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_click_echo: mock.Mock,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        None,
        ChildProcessError,
    )
    ansible_runner.start()

    assert mocked_click_echo.call_args_list == [
        mock.call(config.ANSIBLE_ROLES_MESSAGE),
        mock.call(config.ANSIBLE_COLLECTIONS_MESSAGE),
        mock.call(config.ANSIBLE_INVOKE_MESSAGE),
    ]

  def test_spawn__third_process_fails__logging(
      self,
      ansible_runner: runner.AnsibleRunner,
      mocked_ansible_process: mock.Mock,
      mocked_filesystem: filesystem.FileSystem,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    mocked_ansible_process.return_value.spawn.side_effect = (
        None,
        None,
        ChildProcessError,
    )
    caplog.set_level(logging.DEBUG)

    ansible_runner.start()

    assert decode_logs(caplog.records) == \
        self.create_logging_messages(mocked_filesystem)[0:-1]
