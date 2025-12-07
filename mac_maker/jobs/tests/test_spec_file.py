"""Test the SpecFileJob class."""

from unittest import mock

from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.jobs.spec_file import SpecFileJob


class TestSpecFileJob:
  """Test the SpecFileJob class."""

  def test_initialize__has_correct_inheritance(
      self,
      mocked_spec_file_path: str,
  ) -> None:
    instance = SpecFileJob(mocked_spec_file_path)

    assert isinstance(instance, SpecFileJob)
    assert isinstance(instance, ProvisionerJobBase)

  def test_initialize__assigns_spec_file_path(
      self,
      mocked_spec_file_path: str,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    assert spec_file_job_instance.spec_file.path == mocked_spec_file_path

  def test_initialize_spec_file__loads_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.initialize_spec_file()

    mocked_spec_file.return_value.load.assert_called_once_with()
