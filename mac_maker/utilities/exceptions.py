"""Exceptions for the Mac Maker utilities."""


class GithubExceptionBase(Exception):
  """Base class for GitHub exceptions."""


class GithubCommunicationError(GithubExceptionBase):
  """Raised when a remote GitHub repository cannot be accessed."""


class GithubRepositoryInvalid(GithubExceptionBase):
  """Raised when a GitHub repository URL cannot be parsed."""


class WorkSpaceExceptionBase(Exception):
  """Base class for WorkSpace exceptions."""


class WorkSpaceInvalid(WorkSpaceExceptionBase):
  """Raised when an improperly configured WorkSpace is used."""
