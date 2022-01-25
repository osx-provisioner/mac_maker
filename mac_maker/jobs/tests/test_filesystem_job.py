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
  """Test the FileSystemJob class."""

  def setUp(self) -> None:
    self.mock_path = "/mock/path"
    self.job = jobs_module.FileSystemJob(self.mock_path)

  def test_init(self) -> None:
    self.assertIsInstance(
        self.job.jobspec,
        spec.JobSpec,
    )
    self.assertEqual(self.job.spec_file_location, self.mock_path)


@mock.patch(JOBS_BASES + ".JobSpec.extract_precheck_from_job_spec")
class TestFileSystemJobGetPrecheck(TestCase):
  """Test the FileSystemJob class get_precheck_content method."""

  def setUp(self) -> None:
    self.mock_path = "/mock/path"
    self.job = jobs_module.FileSystemJob(self.mock_path)

  def test_get_precheck_content_return_value(
      self, m_extract: mock.Mock
  ) -> None:
    mock_data = {"a", "b"}
    m_extract.return_value = mock_data

    results = self.job.get_precheck_content()

    self.assertEqual(results, mock_data)

  def test_get_precheck_content_call(self, m_extract: mock.Mock) -> None:

    mock_data = {"a", "b"}
    m_extract.return_value = mock_data

    self.job.get_precheck_content()

    m_extract.assert_called_once_with(self.mock_path)


@mock.patch(JOBS_MODULE + ".click.echo")
@mock.patch(JOBS_BASES + ".JobSpec.read_job_spec_from_filesystem")
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

  def test_get_state_return_value(
      self, m_create: mock.Mock, _: mock.Mock
  ) -> None:
    m_create.return_value = self.mock_spec_content

    results = self.jobs.get_state()

    self.assertEqual(results, self.mock_spec_content['spec_file_content'])

  def test_get_state_echo(self, m_create: mock.Mock, m_echo: mock.Mock) -> None:
    m_create.return_value = self.mock_spec_content

    self.jobs.get_state()

    m_echo.assert_any_call(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    m_echo.assert_any_call(self.mock_spec_content['spec_file_location'])

  def test_get_state_call(self, m_create: mock.Mock, __: mock.Mock) -> None:
    m_create.return_value = self.mock_spec_content

    self.jobs.get_state()

    m_create.assert_called_once_with(
        self.mock_spec_content['spec_file_location']
    )
