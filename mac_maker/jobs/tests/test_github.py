"""Test the GitHubJob class."""

from typing import Optional
from unittest import mock

import pytest
from mac_maker import config
from mac_maker.__helpers__.parametrize import templated_parameters
from mac_maker.jobs.github import GitHubJob


class TestGitHubJob:
  """Test the GitHubJob class."""

  valid_url = "https://github.com/owner/repo.git"
  valid_url_parameterization = pytest.mark.parametrize(
      "url,branch_name",
      templated_parameters(
          (valid_url, None),
          (valid_url, "main"),
          names=[1],
          template="branch:{0}",
      ),
  )

  @valid_url_parameterization
  def test_initialize__valid_url__vary_parameters__has_correct_attributes(
      self,
      url: str,
      branch_name: Optional[str],
  ) -> None:
    instance = GitHubJob(url, branch_name)

    assert instance.branch_name == branch_name
    assert instance.workspace is None

  @valid_url_parameterization
  def test_initialize__valid_url__vary_parameters__has_github_repository(
      self,
      mocked_github_repository: mock.Mock,
      url: str,
      branch_name: Optional[str],
  ) -> None:
    instance = GitHubJob(url, branch_name)

    assert instance.repository == mocked_github_repository.return_value
    mocked_github_repository.assert_called_once_with(url)

  def test_get_precheck_content__creates_workspace_and_finds_spec_file(
      self,
      mocked_workspace: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_precheck_content()

    mocked_workspace.assert_called_once_with()
    mocked_workspace.return_value.add_repository.assert_called_once_with(
        github_job_instance.repository,
        github_job_instance.branch_name,
    )
    mocked_workspace.return_value.add_spec_file.assert_called_once()

  def test_get_precheck_content__reuses_workspace(
      self,
      mocked_workspace: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_precheck_content()
    github_job_instance.get_precheck_content()

    mocked_workspace.assert_called_once_with()

  def test_get_precheck_content__loads_spec_file_data(
      self,
      mocked_spec_file_extractor_instance: mock.Mock,
      mocked_workspace: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_precheck_content()

    mocked_spec_file_extractor_instance \
        .get_spec_file_data.assert_called_once_with(
          str(mocked_workspace.return_value.spec_file)
        )
    assert github_job_instance.loaded_spec_file_data == \
        mocked_spec_file_extractor_instance.get_spec_file_data.return_value

  def test_get_precheck_content__extracts_precheck_data_from_spec_file(
      self,
      mocked_precheck_extractor_instance: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_precheck_content()

    mocked_precheck_extractor_instance \
        .get_precheck_data.assert_called_once_with(
          github_job_instance.loaded_spec_file_data
        )

  def test_get_precheck_content__returns_correct_value(
      self,
      mocked_precheck_extractor_instance: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    results = github_job_instance.get_precheck_content()

    assert results == mocked_precheck_extractor_instance \
        .get_precheck_data.return_value

  def test_get_precheck_content__calls_echo(
      self,
      mocked_click_echo: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_precheck_content()

    assert mocked_click_echo.mock_calls == [
        mock.call(config.ANSIBLE_RETRIEVE_MESSAGE),
    ]

  def test_get_state__creates_workspace_and_finds_spec_file(
      self,
      mocked_workspace: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_state()

    mocked_workspace.assert_called_once_with()
    mocked_workspace.return_value.add_repository.assert_called_once_with(
        github_job_instance.repository,
        github_job_instance.branch_name,
    )
    mocked_workspace.return_value.add_spec_file.assert_called_once()

  def test_get_state__shares_workspace_with_get_precheck_content(
      self,
      mocked_workspace: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_precheck_content()
    github_job_instance.get_state()

    mocked_workspace.assert_called_once_with()

  def test_get_state__reuses_workspace(
      self,
      mocked_workspace: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_state()
    github_job_instance.get_state()

    mocked_workspace.assert_called_once_with()

  def test_get_state__returns_correct_value(
      self,
      github_job_instance: GitHubJob,
  ) -> None:
    results = github_job_instance.get_state()

    assert results == \
        github_job_instance.loaded_spec_file_data['spec_file_content']

  def test_get_state__calls_echo(
      self,
      mocked_click_echo: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.get_state()

    assert mocked_click_echo.mock_calls == [
        mock.call(config.ANSIBLE_RETRIEVE_MESSAGE),
        mock.call(config.SPEC_FILE_CREATED_MESSAGE),
        mock.call(
            github_job_instance.loaded_spec_file_data['spec_file_location']
        )
    ]
