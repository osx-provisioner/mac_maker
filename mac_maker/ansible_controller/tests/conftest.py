"""Test fixtures for the ansible_controllers module."""
# pylint: disable=redefined-outer-name

import os
from typing import Callable, Generator
from unittest import mock

import pytest
from mac_maker.ansible_controller import process, runner
from mac_maker.profile import Profile
from mac_maker.utilities import state


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
def mocked_environment() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_folder() -> str:
  return "/mock/dir1"


@pytest.fixture
def mocked_os_chdir() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_popen(mocked_popen_process: mock.Mock,) -> mock.Mock:
  return mock.Mock(return_value=mocked_popen_process)


@pytest.fixture
def mocked_popen_process() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_profile(mocked_folder: str) -> Profile:
  return Profile(mocked_folder)


@pytest.fixture
def mocked_state() -> state.State:
  return state.State()


@pytest.fixture
def setup_process_module(
    mocked_environment: mock.Mock,
    mocked_os_chdir: mock.Mock,
    mocked_popen: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        process,
        "environment",
        mock.Mock(**{"Environment": mocked_environment}),
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
def ansible_process(
    mocked_profile: Profile,
    mocked_state: state.State,
    setup_process_module: Callable[[], None],
) -> process.AnsibleProcess:
  setup_process_module()

  return process.AnsibleProcess(mocked_state.state_generate(mocked_profile))


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
    mocked_profile: Profile,
    mocked_state: state.State,
    setup_runner_module: Callable[[], None],
) -> runner.AnsibleRunner:
  setup_runner_module()

  return runner.AnsibleRunner(mocked_state.state_generate(mocked_profile))
