"""Test the JobSpec class."""

import json
import os
from logging import Logger
from pathlib import Path
from typing import cast
from unittest import TestCase, mock

from .. import spec, state

SPEC_MODULE = spec.__name__


class TestSpecClass(TestCase):
  """Test the JobSpec class."""

  def setUp(self) -> None:
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = Path("spec.json")
    self.mock_workspace = mock.Mock()
    self.mock_job_spec = {
        'spec_file_content': "some content",
        'spec_file_location': "some location"
    }

  def test_init_settings(self) -> None:
    self.assertIsInstance(
        self.spec.log,
        Logger,
    )
    self.assertIsInstance(
        self.spec.state_manager,
        state.State,
    )


class TestSpecValidity(TestCase):
  """Test the JobSpec class validation methods."""

  def setUp(self) -> None:
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = Path("spec.json")
    self.mock_workspace = mock.Mock()
    self.mock_job_spec = {
        'spec_file_content': "some content",
        'spec_file_location': "some location"
    }
    self.fixtures_folder = Path(os.path.dirname(__file__)) / "fixtures"

  def test_v1_spec(self) -> None:
    v1_mock_spec = self.fixtures_folder / "mock_v1_job_spec.json"
    self.spec.read_job_spec_from_filesystem(v1_mock_spec)

  def test_v1_spec_invalid(self) -> None:
    v1_mock_spec = self.fixtures_folder / "mock_v1_invalid_job_spec.json"

    with self.assertRaises(spec.JobSpecFileException) as exc:
      self.spec.read_job_spec_from_filesystem(v1_mock_spec)

    self.assertListEqual(
        json.loads(exc.exception.args[0]), [
            "'collections_path' is a required property",
            "'roles_path' is a required property",
        ]
    )


class TestSpecCreateSpecFromWorkspace(TestCase):
  """Test the JobSpec class read_job_spec_from_workspace method."""

  def setUp(self) -> None:
    self.spec = spec.JobSpec()
    self.mock_spec_file_location = Path("spec.json")
    self.mock_workspace = mock.Mock()
    self.mock_workspace.repository_root = "root"
    self.mock_state = mock.Mock()
    self.fixtures_folder = Path(os.path.dirname(__file__)) / "fixtures"

    self.spec_fixture = self.fixtures_folder / "mock_v1_job_spec.json"
    with open(self.spec_fixture, encoding="utf-8") as fhandle:
      self.loaded_spec_fixture = json.load(fhandle)

    self.mock_state.state_generate.side_effect = [
        self.loaded_spec_fixture, self.spec_fixture
    ]
    self.spec.state_manager = self.mock_state

  def test_read_job_spec_from_workspace_results(self) -> None:

    results = self.spec.read_job_spec_from_workspace(self.mock_workspace)
    self.assertDictEqual(
        results, {
            'spec_file_content': self.loaded_spec_fixture,
            'spec_file_location': 'root/spec.json',
        }
    )

  def test_read_job_spec_from_workspace_validation(self) -> None:
    self.mock_state.state_generate.side_effect = [
        "Invalid Spec", self.spec_fixture
    ]
    with self.assertRaises(spec.JobSpecFileException):
      self.spec.read_job_spec_from_workspace(self.mock_workspace)


class TestSpecCreateSpecFromFileSystem(TestCase):
  """Test the JobSpec class read_job_spec_from_filesystem method."""

  def setUp(self) -> None:
    self.spec = spec.JobSpec()
    self.fixtures_folder = Path(os.path.dirname(__file__)) / "fixtures"
    self.spec_fixture = self.fixtures_folder / "mock_v1_job_spec.json"
    with open(self.spec_fixture, encoding="utf-8") as fhandle:
      self.loaded_spec_fixture = json.load(fhandle)

  def test_read_job_spec_from_filesystem(self) -> None:

    results = self.spec.read_job_spec_from_filesystem(self.spec_fixture)
    self.assertDictEqual(
        results, {
            'spec_file_content': self.loaded_spec_fixture,
            'spec_file_location': self.spec_fixture,
        }
    )

  @mock.patch(SPEC_MODULE + ".json.load")
  def test_read_job_spec_from_filesystem_validation(
      self, m_load: mock.Mock
  ) -> None:
    m_load.return_value = "Invalid Spec"
    with self.assertRaises(spec.JobSpecFileException):
      self.spec.read_job_spec_from_filesystem(self.spec_fixture)


@mock.patch('builtins.open')
class TestSpecExtractPreCheckFromJobSpec(TestCase):
  """Test the JobSpec class extract_precheck_from_job_spec method."""

  def setUp(self) -> None:
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

  def test_extract_precheck_from_job_spec_rehydrate(
      self, m_open: mock.Mock
  ) -> None:

    m_open.return_value.__enter__.return_value = self.mock_context

    self.mock_state.state_rehydrate.return_value = self.mock_spec_file_content

    self.spec.extract_precheck_from_job_spec(self.mock_spec_file_location)

    cast(mock.Mock, self.spec.state_manager.state_rehydrate).assert_called_with(
        Path(self.mock_spec_file_location)
    )

  def test_extract_precheck_from_job_spec_results(
      self, m_open: mock.Mock
  ) -> None:

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
