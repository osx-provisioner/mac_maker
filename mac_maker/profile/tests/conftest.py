"""Pytest fixtures for the Mac Maker profile."""
# pylint: disable=redefined-outer-name

from pathlib import Path

import pytest
from mac_maker import profile


@pytest.fixture
def mocked_workspace_root() -> Path:
  return Path("/root/dir1")


@pytest.fixture
def profile_instance(mocked_workspace_root: Path) -> profile.Profile:
  return profile.Profile(mocked_workspace_root)
