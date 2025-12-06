# mypy: disable-error-code="misc"
"""The Mac Maker CLI."""

from typing import Optional

import click
from click_shell import shell
from mac_maker import jobs
from mac_maker.utilities.logger import Logger


@shell(  # type: ignore[untyped-decorator]
    prompt='Mac Maker > ',
    intro="Welcome to Mac Maker. (Type 'help' to get started.)",
)
@click.option(
    '--debug', default=False, is_flag=True, help='Enable debug output.'
)
def cli(debug: bool) -> None:
  """Mac Maker CLI."""
  logger = Logger(debug=debug)
  logger.setup()


@cli.group("apply")  # type: ignore[untyped-decorator]
def apply() -> None:
  """Apply an OSX Machine Profile to this system."""


@cli.group("precheck")  # type: ignore[untyped-decorator]
def precheck() -> None:
  """Ensure an OSX Machine Profile is ready to be applied."""


@precheck.command("folder")  # type: ignore[untyped-decorator]
@click.argument('folder_location', type=click.STRING)
def check_from_folder(folder_location: str) -> None:
  """Precheck an OSX Machine Profile from a local filesystem folder.

  FOLDER_LOCATION: The local filesystem path where a machine profile is saved.
  """
  job = jobs.FolderJob(folder_location)
  job.precheck()


@precheck.command("github")  # type: ignore[untyped-decorator]
@click.argument('github_url', type=click.STRING)
@click.option(
    '--branch',
    required=False,
    type=str,
    help="Specific branch (or tag) of the GitHub repo."
)
def check_from_github(github_url: str, branch: Optional[str]) -> None:
  """Precheck an OSX Machine Profile from a public GitHub Repository.

  GITHUB_URL: URL of a GitHub repo containing a machine profile definition.
  """
  job = jobs.GitHubJob(github_url, branch)
  job.precheck()


@precheck.command("spec")  # type: ignore[untyped-decorator]
@click.argument('spec_file', type=click.STRING)
def check_from_spec_file(spec_file: str) -> None:
  """Precheck an OSX Machine Profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file referencing a profile.
  """
  job = jobs.SpecFileJob(spec_file)
  job.precheck()


@apply.command("folder")  # type: ignore[untyped-decorator]
@click.argument('folder_location', type=click.STRING)
def apply_from_folder(folder_location: str) -> None:
  """Apply an OSX Machine Profile from a local filesystem folder.

  FOLDER_LOCATION: The local filesystem path where a machine profile is saved.
  """
  job = jobs.FolderJob(folder_location)
  job.precheck(notes=False)
  job.provision()


@apply.command("github")  # type: ignore[untyped-decorator]
@click.argument('github_url', type=click.STRING)
@click.option(
    '--branch',
    required=False,
    type=str,
    help="Specific branch (or tag) of the GitHub repo."
)
def apply_from_github(github_url: str, branch: Optional[str]) -> None:
  """Apply an OSX Machine Profile from a public GitHub Repository.

  GITHUB_URL: URL of a GitHub repo containing a machine profile definition.
  """
  job = jobs.GitHubJob(github_url, branch)
  job.precheck(notes=False)
  job.provision()


@apply.command("spec")  # type: ignore[untyped-decorator]
@click.argument('spec_file', type=click.STRING)
def apply_from_spec_file(spec_file: str) -> None:
  """Apply an OSX Machine Profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file.
  """
  job = jobs.SpecFileJob(spec_file)
  job.precheck(notes=False)
  job.provision()


@cli.command("version")  # type: ignore[untyped-decorator]
def version() -> None:
  """Report the current Mac Maker version."""
  job = jobs.VersionJob()
  job.invoke()
