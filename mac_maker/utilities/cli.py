"""Utilities for the Mac Maker CLI."""

import sys

import mac_maker.cli


def was_started_without_shell() -> bool:
  """Report whether or not the CLI was started without a shell.

  :returns: A boolean indicating if the CLI was started without a shell.
  """

  for command in mac_maker.cli.\
      cli.commands.keys():
    if command in sys.argv:
      return True
  return False
