"""Version command for the Mac Maker cli."""

import click
import pkg_resources


class VersionCommand:
  """Version command for the Mac Maker cli."""

  def get_version(self) -> None:
    """Report the Mac Maker version."""

    click.echo(
        "Mac Maker Version: "
        f"{pkg_resources.get_distribution('mac_maker').version}",
    )
