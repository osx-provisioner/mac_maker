"""Python interpreter discovery class."""

import os
from pathlib import Path


class InterpreterNotFound(Exception):
  """Raised when a valid Python interpreter is not found."""


class Interpreter:
  """The local Python interpreter used by Ansible."""

  options = [
      Path("/usr/bin/python"),
      Path("/usr/bin/python3"),
  ]

  def get_interpreter_path(self) -> Path:
    """Return the path to a valid python interpreter on this system.

    :returns: The path to a valid python interpreter.
    """

    for interpreter in self.options:
      if os.path.exists(interpreter):
        return interpreter

    raise InterpreterNotFound("No Python interpreter found.")
