"""Pytest fixtures for the Mac Maker utilities."""
# pylint: disable=redefined-outer-name

from pathlib import Path
from typing import Callable, cast
from unittest import mock

import pytest
from mac_maker.utilities import workspace


@pytest.fixture
def mocked_profile_root() -> Path:
  return Path("mocked/profile/root")


@pytest.fixture
def mocked_github_repository(mocked_profile_root: Path,) -> mock.Mock:
  return mock.Mock(
      **{"get_zip_bundle_root_folder.return_value": mocked_profile_root}
  )


@pytest.fixture
def mocked_os_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_spec_file() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_spec_file_instance(mocked_spec_file: mock.Mock) -> mock.Mock:
  return cast(mock.Mock, mocked_spec_file.return_value)


@pytest.fixture
def setup_workspace_module(
    mocked_os_module: mock.Mock,
    mocked_shutil_module: mock.Mock,
    mocked_spec_file: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        workspace,
        "os",
        mocked_os_module,
    )
    monkeypatch.setattr(
        workspace,
        "shutil",
        mocked_shutil_module,
    )
    monkeypatch.setattr(
        workspace.spec_file,
        "SpecFile",
        mocked_spec_file,
    )

  return setup


@pytest.fixture
def workspace_instance(
    setup_workspace_module: Callable[[], None],
) -> workspace.WorkSpace:
  setup_workspace_module()

  return workspace.WorkSpace()


@pytest.fixture
def workspace_instance_with_profile(
    workspace_instance: workspace.WorkSpace,
) -> workspace.WorkSpace:
  workspace_instance.profile_root = Path("/repository/path")

  return workspace_instance
