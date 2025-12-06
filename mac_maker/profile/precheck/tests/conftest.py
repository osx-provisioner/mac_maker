"""Pytest fixtures for Mac Maker profile precheck data."""
# pylint: disable=redefined-outer-name

from typing import Callable
from unittest import mock

import pytest
from mac_maker.profile.precheck import precheck_extractor


@pytest.fixture
def mocked_textfile_read() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_extractor_module(
    mocked_textfile_read: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        precheck_extractor.TextFileReader,
        "read_text_file",
        mocked_textfile_read,
    )

  return setup


@pytest.fixture
def precheck_extractor_instance(
    setup_extractor_module: Callable[[], None],
) -> precheck_extractor.PrecheckExtractor:
  setup_extractor_module()

  return precheck_extractor.PrecheckExtractor()
