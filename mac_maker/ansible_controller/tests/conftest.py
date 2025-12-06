"""Pytest fixtures for the ansible_controllers module."""
# pylint: disable=redefined-outer-name

import os
from typing import Callable, Generator, cast
from unittest import mock

import pytest
from mac_maker.ansible_controller import (
    environment,
    interpreter,
    inventory,
    process,
    runner,
    spec,
)


@pytest.fixture
def mocked_ansible_interpreter() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_ansible_environment() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_ansible_interpreter_instance(
    mocked_ansible_interpreter: mock.Mock
) -> mock.Mock:
  return cast(mock.Mock, mocked_ansible_interpreter.return_value)


@pytest.fixture
def mocked_ansible_process() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_bundle_path() -> str:
  return "/mock/dir2"


@pytest.fixture
def mocked_click_echo() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_command() -> str:
  return "ansible-galaxy install requirements -r requirements.yml"


@pytest.fixture
def mocked_os() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_chdir() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_popen(mocked_popen_process: mock.Mock) -> mock.Mock:
  return mock.Mock(return_value=mocked_popen_process)


@pytest.fixture
def mocked_popen_process() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_textfile_write() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_interpreter_module(
    mocked_os: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        interpreter,
        "os",
        mocked_os,
    )

  return setup


@pytest.fixture
def setup_inventory_module(
    mocked_ansible_interpreter: mock.Mock,
    mocked_os: mock.Mock,
    mocked_textfile_write: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        inventory,
        "AnsibleInterpreter",
        mocked_ansible_interpreter,
    )
    monkeypatch.setattr(
        inventory,
        "os",
        mocked_os,
    )
    monkeypatch.setattr(
        inventory.AnsibleInventoryFile,
        "write_text_file",
        mocked_textfile_write,
    )

  return setup


@pytest.fixture
def setup_process_module(
    mocked_ansible_environment: mock.Mock,
    mocked_os_chdir: mock.Mock,
    mocked_popen: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        process,
        "environment",
        mock.Mock(**{"AnsibleEnvironment": mocked_ansible_environment}),
    )
    monkeypatch.setattr(
        process,
        "os",
        mock.Mock(**{
            "chdir": mocked_os_chdir,
            "path": os.path
        }),
    )
    monkeypatch.setattr(
        process, "subprocess", mock.MagicMock(**{"Popen": mocked_popen})
    )

  return setup


@pytest.fixture
def setup_runner_module(
    mocked_ansible_process: mock.Mock,
    mocked_click_echo: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        runner,
        "click",
        mock.Mock(**{"echo": mocked_click_echo}),
    )
    monkeypatch.setattr(
        runner,
        "process",
        mock.Mock(**{"AnsibleProcess": mocked_ansible_process}),
    )

  return setup


@pytest.fixture
def ansible_environment(
    global_spec_mock: spec.Spec
) -> environment.AnsibleEnvironment:
  return environment.AnsibleEnvironment(global_spec_mock)


@pytest.fixture
def ansible_interpreter(
    setup_interpreter_module: Callable[[], None],
) -> interpreter.AnsibleInterpreter:
  setup_interpreter_module()

  return interpreter.AnsibleInterpreter()


@pytest.fixture
def ansible_inventory(
    global_spec_mock: spec.Spec,
    setup_inventory_module: Callable[[], None],
) -> inventory.AnsibleInventoryFile:
  setup_inventory_module()

  return inventory.AnsibleInventoryFile(global_spec_mock)


@pytest.fixture
def ansible_process(
    global_spec_mock: spec.Spec,
    setup_process_module: Callable[[], None],
) -> process.AnsibleProcess:
  setup_process_module()

  return process.AnsibleProcess(global_spec_mock)


@pytest.fixture
def ansible_process_frozen(
    ansible_process: process.AnsibleProcess,
    mocked_bundle_path: str,
) -> Generator[process.AnsibleProcess, None, None]:
  if (
      getattr(process.sys, "frozen", None)
      or getattr(process.sys, "_MEIPASS", None)
  ):  # nocover
    raise RuntimeError("Unrecognized test state!")

  setattr(process.sys, "frozen", True)
  setattr(process.sys, "_MEIPASS", mocked_bundle_path)

  yield ansible_process

  delattr(process.sys, "frozen")
  delattr(process.sys, "_MEIPASS")


@pytest.fixture
def ansible_runner(
    global_spec_mock: spec.Spec,
    setup_runner_module: Callable[[], None],
) -> runner.AnsibleRunner:
  setup_runner_module()
  return runner.AnsibleRunner(global_spec_mock)
