"""Exceptions for spec files."""


class SpecFileBaseException(Exception):
  """Base class for spec file exceptions."""


class SpecFileContentNotDefined(SpecFileBaseException):
  """Raised when a spec file's content is accessed before being defined."""


class SpecFilePathNotDefined(SpecFileBaseException):
  """Raised when a spec file's path is accessed before being defined."""


class SpecFileValidationError(SpecFileBaseException):
  """Raised when reading an invalid spec file."""
