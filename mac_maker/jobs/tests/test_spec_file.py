"""Test the SpecFileJob class."""

from unittest import mock

from mac_maker import config
from mac_maker.jobs.spec import SpecFileJob


class TestSpecFileJob:
  """Test the SpecFileJob class."""

  def test_initialize__has_correct_attributes(
      self,
      mocked_spec_file_path: str,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    assert spec_file_job_instance.spec_file_location == mocked_spec_file_path
    assert spec_file_job_instance.job_spec_data is None

  def test_get_precheck_content__loads_spec_file_data(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_precheck_content()

    mocked_jobspec_extractor_instance \
        .get_job_spec_data.assert_called_once_with(
          spec_file_job_instance.spec_file_location
        )

  def test_get_precheck_content__reuses_spec_file_data(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_precheck_content()
    spec_file_job_instance.get_precheck_content()

    mocked_jobspec_extractor_instance \
        .get_job_spec_data.assert_called_once_with(
          spec_file_job_instance.spec_file_location
        )

  def test_get_precheck_content__extracts_precheck_data_from_spec_file(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      mocked_precheck_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_precheck_content()

    mocked_precheck_extractor_instance \
        .get_precheck_data.assert_called_once_with(
          mocked_jobspec_extractor_instance.get_job_spec_data.return_value
        )

  def test_get_precheck_content__returns_correct_value(
      self,
      mocked_precheck_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    results = spec_file_job_instance.get_precheck_content()

    assert results == mocked_precheck_extractor_instance \
        .get_precheck_data.return_value

  def test_get_state__loads_spec_file_data(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_state()

    mocked_jobspec_extractor_instance \
        .get_job_spec_data.assert_called_once_with(
          spec_file_job_instance.spec_file_location
        )

  def test_get_state__shares_spec_file_data_with_get_precheck_content(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_precheck_content()
    spec_file_job_instance.get_state()

    mocked_jobspec_extractor_instance \
        .get_job_spec_data.assert_called_once_with(
          spec_file_job_instance.spec_file_location
        )

  def test_get_state__reuses_spec_file_data(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_state()
    spec_file_job_instance.get_state()

    mocked_jobspec_extractor_instance \
        .get_job_spec_data.assert_called_once_with(
          spec_file_job_instance.spec_file_location
        )

  def test_get_state__returns_correct_value(
      self,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    results = spec_file_job_instance.get_state()

    assert results == mocked_jobspec_extractor_instance \
        .get_job_spec_data.return_value['spec_file_content']

  def test_get_state__calls_echo(
      self,
      mocked_click_echo: mock.Mock,
      mocked_jobspec_extractor_instance: mock.Mock,
      spec_file_job_instance: SpecFileJob,
  ) -> None:
    spec_file_job_instance.get_state()

    assert mocked_click_echo.mock_calls == [
        mock.call(config.ANSIBLE_JOB_SPEC_READ_MESSAGE),
        mock.call(
            mocked_jobspec_extractor_instance.get_job_spec_data.
            return_value['spec_file_location']
        )
    ]
