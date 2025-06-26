"""Pytest fixtures for the Mac Maker utilities."""
# pylint: disable=redefined-outer-name

from pathlib import Path
from typing import Callable, cast
from unittest import mock

import pytest
from mac_maker.utilities import workspace


@pytest.fixture
def mocked_repository_root() -> Path:
  return Path("mocked/repository/root")


@pytest.fixture
def mocked_github_repository(mocked_repository_root: Path,) -> mock.Mock:
  return mock.Mock(
      **{"get_zip_bundle_root_folder.return_value": mocked_repository_root}
  )


@pytest.fixture
def mocked_spec_file() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_spec_file_instance(mocked_spec_file: mock.Mock) -> mock.Mock:
  return cast(mock.Mock, mocked_spec_file.return_value)


@pytest.fixture
def setup_workspace_module(
    mocked_spec_file: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(workspace.spec_file, "SpecFile", mocked_spec_file)

  return setup


@pytest.fixture
def workspace_instance(
    setup_workspace_module: Callable[[], None],
) -> workspace.WorkSpace:
  setup_workspace_module()

  return workspace.WorkSpace()


@pytest.fixture
def workspace_instance_with_repository(
    workspace_instance: workspace.WorkSpace,
) -> workspace.WorkSpace:
  workspace_instance.repository_root = Path("/repository/path")

  return workspace_instance
