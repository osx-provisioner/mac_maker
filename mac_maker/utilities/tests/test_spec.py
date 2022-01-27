"""Test the JobSpecExtractor class."""

from logging import Logger
from pathlib import Path
from unittest import TestCase, mock

from ...tests.fixtures import fixtures_spec
from .. import spec, state
from ..validation.spec import SpecFileValidationException

SPEC_MODULE = spec.__name__


class TestSpecClass(TestCase):
  """Test the JobSpecExtractor class."""

  def setUp(self) -> None:
    self.spec = spec.JobSpecExtractor()
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
  """Test the JobSpecExtractor class read_job_spec_from_filesystem method."""

  def setUp(self) -> None:
    super().setUp()
    self.spec = spec.JobSpecExtractor()
    self.spec_fixture = self.fixtures_folder / "mock_v1_job_spec.json"
    self.loaded_spec_fixture = self.json_reader.load_json_file(
        self.spec_fixture
    )

  def test_read_job_spec_from_filesystem(self) -> None:

    results = self.spec.get_job_spec_data(self.spec_fixture)
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
      self.spec.get_job_spec_data(self.spec_fixture)
