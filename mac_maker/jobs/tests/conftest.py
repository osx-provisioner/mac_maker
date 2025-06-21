"""Pytest fixtures for mac_maker job classes."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from mac_maker.jobs import github, spec, version


@pytest.fixture
def mocked_click_echo(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      github,
      "click",
      mock.Mock(echo=instance),
  )
  monkeypatch.setattr(
      spec,
      "click",
      mock.Mock(echo=instance),
  )
  monkeypatch.setattr(
      version,
      "click",
      mock.Mock(echo=instance),
  )
  return instance


@pytest.fixture
def version_job_instance() -> version.VersionJob:
  return version.VersionJob()
