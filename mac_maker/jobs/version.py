"""A simple job to report the version of the Mac Maker CLI."""

from importlib.metadata import version

import click
from mac_maker.jobs.bases.simple import SimpleJobBase


class VersionJob(SimpleJobBase):
  """Version command for the Mac Maker CLI."""

  def invoke(self) -> None:
    """Report the Mac Maker version."""

    click.echo(f"Mac Maker Version: {version('mac_maker')}")
