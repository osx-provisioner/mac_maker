"""GitHub code repository representation."""

import logging
import re
from io import BytesIO
from typing import Dict, Union
from zipfile import ZipFile

import requests
from .. import config


class InvalidGithubRepository(BaseException):
  """Raised when a repository URL cannot be parsed."""


class GithubRepository:
  """GitHub code repository representation."""

  match_http = re.compile(config.GITHUB_HTTP_REGEX, re.IGNORECASE)
  match_ssh = re.compile(config.GITHUB_SSH_REGEX, re.IGNORECASE)
  default_branch = config.GITHUB_DEFAULT_BRANCH

  def __init__(self, repository: str) -> None:
    self.logger = logging.getLogger(config.LOGGER_NAME)
    self._parsed_url = self._parse_repository_url(repository)

  def _parse_repository_url(self, repository: str) -> re.Match:
    parsed_url = re.match(self.match_http, repository)
    if not parsed_url:
      parsed_url = re.match(self.match_ssh, repository)
    if not parsed_url:
      self.logger.error(
          "GithubRepository: Cannot parse github repository url from: %s",
          repository,
      )
      raise InvalidGithubRepository("Invalid GitHub Repository.")
    return parsed_url

  def get_branch_name(self, branch_name: Union[str, None]) -> str:
    """Return the branch name, supporting the default branch.

    :param branch_name: The branch of the repository to use.
    """

    if branch_name is None:
      return self.default_branch
    return branch_name

  def get_repo_name(self) -> str:
    """Return the repo name of the repository."""

    return f"{self._parsed_url.group('repo')}"

  def get_org_name(self) -> str:
    """Return the org (or user) name of the repository."""
    return f"{self._parsed_url.group('org')}"

  def get_http_url(self) -> str:
    """Return the http url for the repository."""

    return (
        f"https://github.com/{self._parsed_url.group('org')}/"
        f"{self._parsed_url.group('repo')}.git"
    )

  def get_ssh_url(self) -> str:
    """Return the ssh url for the repository."""

    return (
        f"git@github.com:{self._parsed_url.group('org')}/"
        f"{self._parsed_url.group('repo')}.git"
    )

  def get_zip_bundle_url(self, branch_name: Union[str, None]) -> str:
    """Generate a zipfile url for the given branch.

    :param branch_name: The branch of the repository to use.
    """

    branch_name = self.get_branch_name(branch_name)
    return (
        f"https://github.com/{self._parsed_url.group('org')}/"
        f"{self._parsed_url.group('repo')}"
        f"/archive/refs/heads/{branch_name}.zip"
    )

  def get_zip_bundle_root_folder(self, branch_name: Union[str, None]) -> str:
    """Return the name of the top level folder inside a repo's zip bundle."""

    branch_name = self.get_branch_name(branch_name)
    return f"{self._parsed_url.group('repo')}-{branch_name}"

  def download_zip_bundle_files(
      self, branch_name: Union[str, None], file_names: Dict[str, str]
  ) -> Dict[str, str]:
    """Download a zip bundle for the branch, then unzip the given files.

    :param branch_name: The branch of the repository to use.
    :param file_names: A dictionary of filenames that will be read.
    """

    results = {}
    branch_name = self.get_branch_name(branch_name)
    http_response = self._download_zipfile(branch_name)
    with ZipFile(BytesIO(http_response.content)) as zipfile:
      for key, file_name in file_names.items():
        results[key] = (
            zipfile.read(
                f"{self._parsed_url.group('repo')}-{branch_name}/"
                f"{file_name}"
            ).decode('utf-8')
        )
    return results

  def download_zip_bundle_profile(
      self, file_system_target: str, branch_name: Union[str, None]
  ) -> None:
    """Download a zip bundle for the branch, then unzip everything.

    :param branch_name: The branch of the repository to use.
    :param file_system_target: The destination path to unzip the bundle to.
    """

    branch_name = self.get_branch_name(branch_name)
    http_response = self._download_zipfile(branch_name)
    with ZipFile(BytesIO(http_response.content)) as zipfile:
      zipfile.extractall(path=file_system_target)

  def _download_zipfile(self, branch_name: str) -> requests.Response:
    remote_url = self.get_zip_bundle_url(branch_name)
    http_response = requests.get(remote_url)
    self.logger.info(
        "GithubRepository: Retrieved zip content from: %s",
        remote_url,
    )
    return http_response
