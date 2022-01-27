"""Test the FileSystemJob class."""

from typing import cast
from unittest import TestCase, mock

from ... import config
from ...jobs import bases as jobs_bases
from ...jobs import filesystem as jobs_module
from ...utilities import spec

JOBS_MODULE = jobs_module.__name__
JOBS_BASES = jobs_bases.__name__


class TestFileSystemJob(TestCase):
  """Test the FileSystemJob class instantiation."""

  def setUp(self) -> None:
    self.mock_path = "/mock/path"
    self.job = jobs_module.FileSystemJob(self.mock_path)

  def test_init(self) -> None:
    self.assertEqual(self.job.spec_file_location, self.mock_path)
    self.assertIsNone(self.job.job_spec_data)


@mock.patch(JOBS_BASES + ".JobSpecExtractor.get_job_spec_data")
@mock.patch(JOBS_BASES + ".PrecheckExtractor.get_precheck_data")
class TestFileSystemJobGetPrecheck(TestCase):
  """Test the FileSystemJob class get_precheck_content method."""

  def setUp(self) -> None:
    self.mock_path = "/mock/path"
    self.job = jobs_module.FileSystemJob(self.mock_path)
    self.mock_data1 = {
        "a": "b"
    }
    self.mock_data2 = {
        "b": "c"
    }

  def test_get_precheck_content_return_value(
      self, m_precheck: mock.Mock, m_job: mock.Mock
  ) -> None:
    m_job.return_value = self.mock_data1
    m_precheck.return_value = self.mock_data2

    results = self.job.get_precheck_content()

    self.assertEqual(self.job.job_spec_data, self.mock_data1)
    self.assertEqual(results, self.mock_data2)

  def test_get_precheck_content_call(
      self, _: mock.Mock, m_job: mock.Mock
  ) -> None:
    self.job.get_precheck_content()
    m_job.assert_called_once_with(self.mock_path)


@mock.patch(JOBS_MODULE + ".click.echo")
@mock.patch(JOBS_BASES + ".JobSpecExtractor.get_job_spec_data")
class TestFileSystemJobGetStateCase(TestCase):
  """Test the FileSystemJob class get_state method."""

  def setUp(self) -> None:
    self.mock_path = "/mock/path"
    self.jobs = jobs_module.FileSystemJob(self.mock_path)
    self.mock_spec_content = cast(
        spec.TypeSpecFileData, {
            'spec_file_content': {'a', 'b'},
            'spec_file_location': self.mock_path
        }
    )

  def test_get_state_return_value(self, m_job: mock.Mock, _: mock.Mock) -> None:
    m_job.return_value = self.mock_spec_content

    results = self.jobs.get_state()

    self.assertEqual(results, self.mock_spec_content['spec_file_content'])

  def test_get_state_echo(self, m_job: mock.Mock, m_echo: mock.Mock) -> None:
    m_job.return_value = self.mock_spec_content

    self.jobs.get_state()

    m_echo.assert_any_call(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    m_echo.assert_any_call(self.mock_spec_content['spec_file_location'])

  def test_get_state_call(self, m_job: mock.Mock, __: mock.Mock) -> None:
    m_job.return_value = self.mock_spec_content

    self.jobs.get_state()

    m_job.assert_called_once_with(self.mock_spec_content['spec_file_location'])

  def test_get_state_spec_not_extracted_twice(
      self, m_job: mock.Mock, __: mock.Mock
  ) -> None:
    m_job.return_value = self.mock_spec_content

    self.jobs.get_state()
    self.jobs.get_state()

    m_job.assert_called_once_with(self.mock_spec_content['spec_file_location'])
