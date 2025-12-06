"""Exceptions for the Ansible controller."""


class AnsibleBaseException(Exception):
  """Base class for Ansible controller exceptions."""


class AnsibleInterpreterNotFound(AnsibleBaseException):
  """Raised when a valid Python interpreter is not found."""
