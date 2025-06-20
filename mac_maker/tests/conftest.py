"""Pytest fixtures for mac_maker cli."""
from typing import Protocol, Tuple, Union, cast
from unittest import mock

import pytest
from click.testing import CliRunner
from mac_maker import cli


class InvokeType(Protocol):

  def __call__(
      self,
      command: str,
      global_flags: Union[Tuple[()], Tuple[str, ...]] = (),
  ) -> None:
    ...


@pytest.fixture
def mocked_job(request: pytest.FixtureRequest) -> mock.Mock:
  return cast(
      mock.Mock,
      request.getfixturevalue(request.param),  # type: ignore[attr-defined]
  )


@pytest.fixture
def mocked_job_github(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(cli.jobs, "GitHubJob", instance)
  return instance


@pytest.fixture
def mocked_job_spec_file(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(cli.jobs, "SpecFileJob", instance)
  return instance


@pytest.fixture
def mocked_job_version(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(cli.jobs, "VersionJob", instance)
  return instance


@pytest.fixture
def mocked_logger(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(cli, "Logger", instance)
  return instance


@pytest.fixture
def invoke() -> InvokeType:
  configured_global_flags = {
      "debug": "--debug"
  }

  def invoker(
      command: str,
      global_flags: Union[Tuple[()], Tuple[str, ...]] = (),
  ) -> None:
    for global_flag in global_flags:
      command = configured_global_flags[global_flag] + " " + command

    runner = CliRunner()
    runner.invoke(cli.cli, args=command)

  return invoker
