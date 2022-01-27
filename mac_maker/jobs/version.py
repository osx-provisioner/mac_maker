"""A simple job to report the version of the Mac Maker CLI."""

import click
import pkg_resources
from . import bases


class VersionJob(bases.SimpleJobBase):
  """Version command for the Mac Maker CLI."""

  def invoke(self) -> None:
    """Report the Mac Maker version."""

    click.echo(
        "Mac Maker Version: "
        f"{pkg_resources.get_distribution('mac_maker').version}",
    )
