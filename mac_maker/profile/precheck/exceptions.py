"""Exceptions for a profile's precheck data."""


class PrecheckBaseException(Exception):
  """Base class for precheck exceptions."""


class PrecheckValidationError(PrecheckBaseException):
  """Raised when reading an invalid precheck environment configuration file."""
