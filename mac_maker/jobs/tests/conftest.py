"""Pytest fixtures for mac_maker job classes."""
# pylint: disable=redefined-outer-name

from typing import cast
from unittest import mock

import pytest
from mac_maker.jobs import github, spec, version
from mac_maker.jobs.bases import provisioner


@pytest.fixture
def mocked_click_echo(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      github,
      "click",
      mock.Mock(echo=instance),
  )
  monkeypatch.setattr(
      spec,
      "click",
      mock.Mock(echo=instance),
  )
  monkeypatch.setattr(
      version,
      "click",
      mock.Mock(echo=instance),
  )
  return instance


@pytest.fixture
def mocked_github_repository(monkeypatch: pytest.MonkeyPatch,) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      github,
      "GithubRepository",
      instance,
  )
  return instance


@pytest.fixture
def mocked_jobspec_extractor(
    global_spec_file_mock: spec.TypeSpecFileData,
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:
  instance = mock.Mock()
  instance.return_value.get_job_spec_data.return_value = global_spec_file_mock
  monkeypatch.setattr(
      provisioner,
      "JobSpecExtractor",
      instance,
  )
  return instance


@pytest.fixture
def mocked_jobspec_extractor_instance(
    mocked_jobspec_extractor: mock.Mock,
) -> mock.Mock:
  return cast(mock.Mock, mocked_jobspec_extractor.return_value)


@pytest.fixture
def mocked_precheck_extractor(monkeypatch: pytest.MonkeyPatch,) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      provisioner,
      "PrecheckExtractor",
      instance,
  )
  return instance


@pytest.fixture
def mocked_precheck_extractor_instance(
    mocked_precheck_extractor: mock.Mock,
) -> mock.Mock:
  return cast(mock.Mock, mocked_precheck_extractor.return_value)


@pytest.fixture
def mocked_spec_file_path() -> str:
  return "/path/to/spec/file"


@pytest.fixture
def mocked_workspace(monkeypatch: pytest.MonkeyPatch,) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      github,
      "WorkSpace",
      instance,
  )
  return instance


@pytest.fixture
def setup_provisioner_mocks(
    # pylint: disable=unused-argument
    mocked_click_echo: mock.Mock,
    mocked_jobspec_extractor: mock.Mock,
    mocked_precheck_extractor: mock.Mock,
) -> None:
  return None


@pytest.fixture
def github_job_instance(
    # pylint: disable=unused-argument
    global_git_branch_mock: str,
    global_git_url_mock: str,
    mocked_github_repository: mock.Mock,
    mocked_workspace: mock.Mock,
    setup_provisioner_mocks: None,
) -> github.GitHubJob:
  return github.GitHubJob(
      global_git_url_mock,
      global_git_branch_mock,
  )


@pytest.fixture
def spec_file_job_instance(
    # pylint: disable=unused-argument
    mocked_spec_file_path: str,
    setup_provisioner_mocks: None,
) -> spec.SpecFileJob:
  return spec.SpecFileJob(mocked_spec_file_path)


@pytest.fixture
def version_job_instance() -> version.VersionJob:
  return version.VersionJob()
