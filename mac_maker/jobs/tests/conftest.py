"""Pytest fixtures for mac_maker job classes."""
# pylint: disable=redefined-outer-name

from typing import Callable
from unittest import mock

import pytest
from mac_maker.jobs import folder, github, spec_file, version
from mac_maker.jobs.bases import provisioner
from mac_maker.profile.spec_file import SpecFile


@pytest.fixture
def mocked_click_echo() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_folder_path() -> str:
  return "/path/to/folder"


@pytest.fixture
def mocked_github_repository() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_precheck_extractor() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_spec_file(global_spec_file_mock: SpecFile) -> mock.Mock:
  return mock.Mock(return_value=global_spec_file_mock)


@pytest.fixture
def mocked_spec_file_path() -> str:
  return "/path/to/spec/file"


@pytest.fixture
def mocked_workspace() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def setup_folder_job_module(
    mocked_click_echo: mock.Mock,
    mocked_spec_file: mock.Mock,
    mocked_workspace: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        folder,
        "click",
        mock.Mock(echo=mocked_click_echo),
    )
    monkeypatch.setattr(
        provisioner,
        "SpecFile",
        mocked_spec_file,
    )
    monkeypatch.setattr(
        folder,
        "WorkSpace",
        mocked_workspace,
    )

  return setup


@pytest.fixture
def setup_github_job_module(
    mocked_click_echo: mock.Mock,
    mocked_github_repository: mock.Mock,
    mocked_spec_file: mock.Mock,
    mocked_workspace: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        github,
        "click",
        mock.Mock(echo=mocked_click_echo),
    )
    monkeypatch.setattr(
        github,
        "GithubRepository",
        mocked_github_repository,
    )
    monkeypatch.setattr(
        provisioner,
        "SpecFile",
        mocked_spec_file,
    )
    monkeypatch.setattr(
        github,
        "WorkSpace",
        mocked_workspace,
    )

  return setup


@pytest.fixture
def setup_spec_file_job_module(
    mocked_click_echo: mock.Mock,
    mocked_precheck_extractor: mock.Mock,
    mocked_spec_file: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        provisioner,
        "click",
        mock.Mock(echo=mocked_click_echo),
    )
    monkeypatch.setattr(
        provisioner,
        "PrecheckExtractor",
        mocked_precheck_extractor,
    )
    monkeypatch.setattr(
        provisioner,
        "SpecFile",
        mocked_spec_file,
    )

  return setup


@pytest.fixture
def setup_version_job_module(
    mocked_click_echo: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        version,
        "click",
        mock.Mock(echo=mocked_click_echo),
    )

  return setup


@pytest.fixture
def folder_job_instance(
    mocked_folder_path: str,
    setup_folder_job_module: Callable[[], None],
) -> folder.FolderJob:
  setup_folder_job_module()

  return folder.FolderJob(mocked_folder_path)


@pytest.fixture
def github_job_instance(
    global_git_branch_mock: str,
    global_git_url_mock: str,
    setup_github_job_module: Callable[[], None],
) -> github.GitHubJob:
  setup_github_job_module()

  return github.GitHubJob(
      global_git_url_mock,
      global_git_branch_mock,
  )


@pytest.fixture
def spec_file_job_instance(
    mocked_spec_file_path: str,
    setup_spec_file_job_module: Callable[[], None],
) -> spec_file.SpecFileJob:
  setup_spec_file_job_module()

  return spec_file.SpecFileJob(mocked_spec_file_path)


@pytest.fixture
def version_job_instance(
    setup_version_job_module: Callable[[], None],
) -> version.VersionJob:
  setup_version_job_module()

  return version.VersionJob()
