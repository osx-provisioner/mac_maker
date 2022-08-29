"""GitHub Repository representation."""

import logging
import re
from io import BytesIO
from pathlib import Path
from typing import Match, Optional, Union
from zipfile import ZipFile

import requests
from .. import config


class InvalidGithubRepository(Exception):
  """Raised when a Github repository URL cannot be parsed."""


class GithubCommunicationError(Exception):
  """Raised when a remote Github repository cannot be accessed."""


class GithubRepository:
  """GitHub Repository representation.

  :param repository: The http or ssh URL of the repository.
  """

  match_http = re.compile(config.GITHUB_HTTP_REGEX, re.IGNORECASE)
  match_ssh = re.compile(config.GITHUB_SSH_REGEX, re.IGNORECASE)
  default_branch = config.GITHUB_DEFAULT_BRANCH
  timeout = 10

  def __init__(self, repository: str) -> None:
    self.logger = logging.getLogger(config.LOGGER_NAME)
    self._parsed_url = self._parse_repository_url(repository)

  def _parse_repository_url(self, repository: str) -> Match[str]:
    parsed_url = re.match(self.match_http, repository)
    if not parsed_url:
      parsed_url = re.match(self.match_ssh, repository)
    if not parsed_url:
      self.logger.error(
          "GithubRepository: Cannot parse a Github Repository URL from: %s",
          repository,
      )
      raise InvalidGithubRepository("Invalid GitHub Repository.")
    return parsed_url

  def get_branch_name(self, branch_name: Optional[str]) -> str:
    """Return the given branch name, or the default branch.

    :param branch_name: The branch of the repository to use.
    :returns: The given branch name, or the default branch.
    """

    if branch_name is None:
      return self.default_branch
    return branch_name

  def get_repo_name(self) -> str:
    """Return Github's name for the repository.

    :return: The name of the repository.
    """

    return f"{self._parsed_url.group('repo')}"

  def get_org_name(self) -> str:
    """Return Github's org (or user) name for the repository.

    :return: The org (or user) name of the repository.
    """
    return f"{self._parsed_url.group('org')}"

  def get_http_url(self) -> str:
    """Return the http url for the repository.

    :return: The http url of the repository.
    """
    return (
        f"https://github.com/{self._parsed_url.group('org')}/"
        f"{self._parsed_url.group('repo')}.git"
    )

  def get_ssh_url(self) -> str:
    """Return the ssh url for the repository.

    :return: The ssh url of the repository.
    """
    return (
        f"git@github.com:{self._parsed_url.group('org')}/"
        f"{self._parsed_url.group('repo')}.git"
    )

  def get_zip_bundle_url(self, branch_name: Optional[str]) -> str:
    """Generate a zipfile url for the given branch.

    :param branch_name: The branch of the repository to use.
    :return: The url of the zipfile bundle for this branch.
    """
    branch_name = self.get_branch_name(branch_name)
    return (
        f"https://github.com/{self._parsed_url.group('org')}/"
        f"{self._parsed_url.group('repo')}"
        f"/archive/refs/heads/{branch_name}.zip"
    )

  def get_zip_bundle_root_folder(self, branch_name: Optional[str]) -> str:
    """Return the top level folder inside a repo's zip bundle.

    :param branch_name: The branch of the repository to use.
    :return: The top level folder inside a repo's zip bundle.
    """
    branch_name = self.get_branch_name(branch_name)
    return f"{self._parsed_url.group('repo')}-{branch_name}"

  def download_zip_bundle_profile(
      self, file_system_target: Union[Path, str], branch_name: Optional[str]
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
    try:
      http_response = requests.get(remote_url, timeout=self.timeout)
    except requests.exceptions.RequestException as exc:
      self.logger.error(
          "GithubRepository: cannot download '%s'",
          remote_url,
      )
      raise GithubCommunicationError(
          "Communication error with Github."
      ) from exc
    self.logger.info(
        "GithubRepository: Retrieved zip content from: %s",
        remote_url,
    )
    return http_response
