"""Test the GitHubJob class."""

from typing import Callable, Optional
from unittest import mock

import pytest
from mac_maker.__helpers__.parametrize import templated_parameters
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
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
  def test_initialize__valid_url__vary_parameters__has_correct_inheritance(
      self,
      url: str,
      branch_name: Optional[str],
  ) -> None:
    instance = GitHubJob(url, branch_name)

    assert isinstance(instance, GitHubJob)
    assert isinstance(instance, ProvisionerJobBase)

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
      setup_github_job_module: Callable[[], None],
      url: str,
      branch_name: Optional[str],
  ) -> None:
    setup_github_job_module()

    instance = GitHubJob(url, branch_name)

    assert instance.repository == mocked_github_repository.return_value
    mocked_github_repository.assert_called_once_with(url)

  def test_initialize_spec_file__calls_echo(
      self,
      mocked_click_echo: mock.Mock,
      github_job_instance: GitHubJob,
  ) -> None:
    github_job_instance.initialize_spec_file()

    mocked_click_echo.assert_called_once_with(
        github_job_instance.Messages.retrieve_github_profile
    )

  @valid_url_parameterization
  def test_initialize_spec_file__creates_workspace(
      self,
      mocked_workspace: mock.Mock,
      setup_github_job_module: Callable[[], None],
      url: str,
      branch_name: Optional[str],
  ) -> None:
    setup_github_job_module()
    instance = GitHubJob(url, branch_name)

    instance.initialize_spec_file()

    mocked_workspace.assert_called_once_with()
    assert instance.workspace == mocked_workspace.return_value

  @valid_url_parameterization
  def test_initialize_spec_file__adds_repository_to_workspace(
      self,
      mocked_workspace: mock.Mock,
      setup_github_job_module: Callable[[], None],
      url: str,
      branch_name: Optional[str],
  ) -> None:
    setup_github_job_module()
    instance = GitHubJob(url, branch_name)

    instance.initialize_spec_file()

    mocked_workspace.return_value.add_repository.assert_called_once_with(
        instance.repository,
        branch_name,
    )

  @valid_url_parameterization
  def test_initialize_spec_file__adds_spec_file_to_workspace(
      self,
      mocked_workspace: mock.Mock,
      setup_github_job_module: Callable[[], None],
      url: str,
      branch_name: Optional[str],
  ) -> None:
    setup_github_job_module()
    instance = GitHubJob(url, branch_name)

    instance.initialize_spec_file()

    mocked_workspace.return_value.add_spec_file.assert_called_once_with()

  @valid_url_parameterization
  def test_initialize_spec_file__initializes_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      setup_github_job_module: Callable[[], None],
      url: str,
      branch_name: Optional[str],
  ) -> None:
    setup_github_job_module()
    instance = GitHubJob(url, branch_name)

    instance.initialize_spec_file()

    assert instance.workspace is not None
    assert mocked_spec_file.return_value.path == \
        str(instance.workspace.spec_file)

  @valid_url_parameterization
  def test_initialize_spec_file__loads_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      setup_github_job_module: Callable[[], None],
      url: str,
      branch_name: Optional[str],
  ) -> None:
    setup_github_job_module()
    instance = GitHubJob(url, branch_name)

    instance.initialize_spec_file()

    mocked_spec_file.return_value.load.assert_called_once_with()
