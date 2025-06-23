"""Exceptions for spec files."""


class SpecFileValidationException(Exception):
  """Raised when reading an invalid spec file."""


class SpecFileNotDefined(Exception):
  """Raised when a spec file's attributes are accessed before being defined."""
