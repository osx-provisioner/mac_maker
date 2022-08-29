"""Test the GithubRepository class."""

from io import BytesIO
from unittest import mock

import requests.exceptions
from ...tests.fixtures import fixtures_git
from .. import github as github_module
from ..github import (
    GithubCommunicationError,
    GithubRepository,
    InvalidGithubRepository,
)

GITHUB_MODULE = github_module.__name__


class TestGithubRepositoryInitialize(fixtures_git.GitTestHarness):
  """Test the initialization of the GithubRepository class."""

  def test_initialize_with_illegal_url(self) -> None:
    with self.assertRaises(InvalidGithubRepository):
      GithubRepository("not a valid url")

  def test_initialize_with_http(self) -> None:
    repo = GithubRepository(self.repository_http_url)
    self.assertEqual(repo.get_http_url(), self.repository_http_url)
    self.assertEqual(repo.get_ssh_url(), self.repository_ssh_url)

  def test_initialize_with_http_truncated(self) -> None:
    url = f"https://github.com/{self.org_name}/" f"{self.repo_name}"

    repo = GithubRepository(url)
    self.assertEqual(repo.get_http_url(), self.repository_http_url)
    self.assertEqual(repo.get_ssh_url(), self.repository_ssh_url)

  def test_initialize_with_ssh(self) -> None:
    repo = GithubRepository(self.repository_ssh_url)
    self.assertEqual(repo.get_http_url(), self.repository_http_url)
    self.assertEqual(repo.get_ssh_url(), self.repository_ssh_url)

  def test_initialize_with_ssh_truncated(self) -> None:
    url = f"git@github.com:{self.org_name}/{self.repo_name}"

    repo = GithubRepository(url)
    self.assertEqual(repo.get_http_url(), self.repository_http_url)
    self.assertEqual(repo.get_ssh_url(), self.repository_ssh_url)


class TestGithubRepositoryGetMethods(fixtures_git.GitTestHarness):
  """Test the get methods of the GithubRepository class."""

  def setUp(self) -> None:
    super().setUp()
    self.repo = GithubRepository(self.repository_http_url)

  def test_zip_archive_url_specific_branch(self) -> None:
    self.assertEqual(
        self.repo.get_zip_bundle_url("develop"),
        "https://github.com/grocerypanic/panic/archive/refs/heads/develop.zip"
    )

  def test_get_branch_name(self) -> None:
    self.assertEqual(self.repo.get_branch_name(None), self.repo.default_branch)

  def test_get_branch_name_specific(self) -> None:
    self.assertEqual(self.repo.get_branch_name("development"), "development")

  def test_get_repo_name(self) -> None:
    self.assertEqual(self.repo.get_repo_name(), self.repo_name)

  def test_get_org_name(self) -> None:
    self.assertEqual(self.repo.get_org_name(), self.org_name)

  def test_get_zip_bundle_root_folder(self) -> None:
    self.assertEqual(
        self.repo.get_zip_bundle_root_folder(None),
        f"{self.repo_name}-{self.repo.default_branch}",
    )

  def test_get_zip_bundle_root_specific(self) -> None:
    branch = "develop"
    self.assertEqual(
        self.repo.get_zip_bundle_root_folder(branch),
        f"{self.repo_name}-{branch}",
    )


@mock.patch(GITHUB_MODULE + ".requests.get")
@mock.patch(GITHUB_MODULE + ".BytesIO")
@mock.patch(GITHUB_MODULE + ".ZipFile")
class TestGithubRepositoryNetwork(fixtures_git.GitTestHarness):
  """Test the GithubRepository classes network bound methods."""

  def setUp(self) -> None:
    super().setUp()
    self.mock_zip_context = mock.Mock()
    self.mock_data = b"Random String"
    self.mock_files = {
        "a": "a.txt",
        "b": "b.txt"
    }
    self.mock_branch = "develop"

  def create_mock_context(
      self, mock_zipfile: mock.Mock, mock_bytes: mock.Mock
  ) -> None:
    context = mock_zipfile.return_value.__enter__
    context.return_value = self.mock_zip_context
    context.return_value.read.return_value = self.mock_data
    mock_bytes.return_value = BytesIO(self.mock_data)

  def test_download_zip_bundle_request(
      self, mock_zipfile: mock.Mock, mock_bytes: mock.Mock, mock_get: mock.Mock
  ) -> None:
    self.create_mock_context(mock_zipfile, mock_bytes)
    mock_folder = "/some_folder"
    mock_branch = "develop"

    repo = GithubRepository(self.repository_http_url)
    repo.download_zip_bundle_profile(mock_folder, mock_branch)

    mock_get.assert_called_once_with(
        repo.get_zip_bundle_url(mock_branch),
        timeout=repo.timeout,
    )

  def test_download_zip_bundle_request_fails(
      self, mock_zipfile: mock.Mock, mock_bytes: mock.Mock, mock_get: mock.Mock
  ) -> None:
    self.create_mock_context(mock_zipfile, mock_bytes)
    mock_folder = "/some_folder"
    mock_branch = "develop"
    mock_get.side_effect = requests.exceptions.RequestException

    repo = GithubRepository(self.repository_http_url)

    with self.assertRaises(GithubCommunicationError):
      repo.download_zip_bundle_profile(mock_folder, mock_branch)

    mock_get.assert_called_once_with(
        repo.get_zip_bundle_url(mock_branch),
        timeout=repo.timeout,
    )

  def test_download_zip_bundle_zipfile_context(
      self, mock_zipfile: mock.Mock, mock_bytes: mock.Mock, _: mock.Mock
  ) -> None:
    self.create_mock_context(mock_zipfile, mock_bytes)
    mock_folder = "/some_folder"
    mock_branch = "develop"

    repo = GithubRepository(self.repository_http_url)
    repo.download_zip_bundle_profile(mock_folder, mock_branch)

    mock_zipfile.assert_called_once_with(mock_bytes.return_value)
    self.mock_zip_context.extractall.assert_called_once_with(path=mock_folder)
