"""A simple job to report the version of the Mac Maker CLI."""

from importlib.metadata import version

import click
from mac_maker.jobs.bases.simple import SimpleJobBase


class VersionJob(SimpleJobBase):
  """Version command for the Mac Maker CLI."""

  class Messages:
    version_string = "Mac Maker Version: %s"

  def invoke(self) -> None:
    """Report the Mac Maker version."""

    click.echo(self.Messages.version_string % version('mac_maker'))
