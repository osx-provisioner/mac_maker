"""Test the JobSpec class."""

from io import StringIO
from logging import Logger
from pathlib import Path
from unittest import TestCase, mock

from .. import spec, state

SPEC_MODULE = spec.__name__


class TestSpecClass(TestCase):
  """Test the JobSpec class."""

  def setUp(self):
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = Path("spec.json")
    self.mock_workspace = mock.Mock()
    self.mock_job_spec = {
        'spec_file_content': "some content",
        'spec_file_location': "some location"
    }

  def test_init_settings(self):
    self.assertIsInstance(
        self.spec.log,
        Logger,
    )
    self.assertIsInstance(
        self.spec.state_manager,
        state.State,
    )


@mock.patch(SPEC_MODULE + '.FileSystem')
class TestSpecCreateSpecFromGithub(TestCase):
  """Test the JobSpec class create_job_spec_from_github method."""

  def setUp(self):
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = Path("spec.json")
    self.mock_workspace = mock.Mock()
    self.mock_state = mock.Mock()

    self.spec.state_manager = self.mock_state

  def test_create_job_spec_from_github_results(self, m_fs):

    results = self.spec.create_job_spec_from_github(self.mock_workspace)
    self.assertEqual(
        results, {
            'spec_file_content': self.mock_state.state_generate.return_value,
            'spec_file_location': m_fs.return_value.get_spec_file.return_value
        }
    )


@mock.patch('builtins.open')
class TestSpecCreateSpecFromFileSystem(TestCase):
  """Test the JobSpec class create_job_spec_from_filesystem method."""

  def setUp(self):
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = "/root/dir1/spec.json"

  def test_create_job_spec_from_github_results(self, m_open):

    m_open.return_value.__enter__.return_value = StringIO('{"one": "two"}')
    results = self.spec.create_job_spec_from_filesystem(
        self.mock_spec_file_location
    )

    self.assertEqual(
        results, {
            'spec_file_content': {
                "one": "two"
            },
            'spec_file_location': self.mock_spec_file_location,
        }
    )


@mock.patch('builtins.open')
class TestSpecExtractPreCheckFromJobSpec(TestCase):
  """Test the JobSpec class extract_precheck_from_job_spec method."""

  def setUp(self):
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = "/root/dir1/spec.json"
    self.mock_state = mock.Mock()
    self.mock_spec_file_content = {
        "workspace_root_path": "/root/dir1"
    }

    self.spec.state_manager = self.mock_state
    self.mock_notes = "notes content"
    self.mock_env = "env content"

    self.mock_context = mock.Mock()
    self.mock_context.read.side_effect = [self.mock_notes, self.mock_env]

  def test_extract_precheck_from_job_spec_rehydrate(self, m_open):

    m_open.return_value.__enter__.return_value = self.mock_context

    self.mock_state.state_rehydrate.return_value = self.mock_spec_file_content

    self.spec.extract_precheck_from_job_spec(self.mock_spec_file_location)

    self.spec.state_manager.state_rehydrate.assert_called_with(
        Path(self.mock_spec_file_location)
    )

  def test_extract_precheck_from_job_spec_results(self, m_open):

    m_open.return_value.__enter__.return_value = self.mock_context

    self.mock_state.state_rehydrate.return_value = self.mock_spec_file_content

    results = self.spec.extract_precheck_from_job_spec(
        self.mock_spec_file_location,
    )

    self.assertDictEqual(
        results,
        {
            'notes': self.mock_notes,
            'env': self.mock_env
        },
    )
