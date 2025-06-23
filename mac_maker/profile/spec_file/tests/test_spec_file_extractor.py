"""Test the SpecFileExtractor class."""

from logging import Logger
from pathlib import Path
from unittest import TestCase, mock

from mac_maker.profile.spec_file import spec_file_extractor
from mac_maker.profile.spec_file.spec_file_validator import (
    SpecFileValidationException,
)
from mac_maker.tests.fixtures import fixtures_spec
from mac_maker.utilities import state

SPEC_MODULE = spec_file_extractor.__name__


class TestSpecClass(TestCase):
  """Test the SpecFileExtractor class."""

  def setUp(self) -> None:
    self.spec = spec_file_extractor.SpecFileExtractor()
    self.mock_spec_file_location = Path("spec.json")

  def test_init_settings(self) -> None:
    self.assertIsInstance(
        self.spec.log,
        Logger,
    )
    self.assertIsInstance(
        self.spec.state_manager,
        state.State,
    )


class TestSpecReadSpecFromFileSystem(fixtures_spec.SpecFileTestHarness):
  """Test the SpecFileExtractor class get_spec_file_data method."""

  def setUp(self) -> None:
    super().setUp()
    self.spec = spec_file_extractor.SpecFileExtractor()
    self.spec_fixture = self.fixtures_folder / "mock_v1_spec_file.json"
    self.loaded_spec_fixture = self.json_reader.load_json_file(
        self.spec_fixture
    )

  def test_read_job_spec_from_filesystem(self) -> None:

    results = self.spec.get_spec_file_data(self.spec_fixture)
    self.assertDictEqual(
        results, {
            'spec_file_content': self.loaded_spec_fixture,
            'spec_file_location': self.spec_fixture,
        }
    )

  @mock.patch(SPEC_MODULE + ".State.state_rehydrate")
  def test_read_job_spec_from_filesystem_invalid(
      self, m_rehydrate: mock.Mock
  ) -> None:
    m_rehydrate.return_value = 'Invalid Spec'
    with self.assertRaises(SpecFileValidationException):
      self.spec.get_spec_file_data(self.spec_fixture)
