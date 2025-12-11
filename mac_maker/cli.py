# mypy: disable-error-code="misc"
"""The Mac Maker CLI."""

from typing import Optional

import click
from click_shell import shell
from mac_maker import jobs
from mac_maker.utilities.logger import Logger

cli_argument_directory = click.Path(
    exists=True,
    dir_okay=True,
    file_okay=False,
    readable=True,
)

cli_argument_file = click.Path(
    exists=True,
    dir_okay=False,
    file_okay=True,
    readable=True,
)


@shell(  # type: ignore[untyped-decorator]
    prompt='Mac Maker > ',
    intro="Welcome to Mac Maker. (Type 'help' to get started.)",
)
@click.option(
    '--debug',
    default=False,
    is_flag=True,
    help='Enable debug output.',
)
def cli(debug: bool) -> None:
  """Mac Maker CLI."""
  logger = Logger(debug=debug)
  logger.setup()


@cli.group(  # type: ignore[untyped-decorator]
    "apply",
    short_help="Apply an OSX Machine Profile to this system.",
)
def apply() -> None:
  """Apply an OSX Machine Profile to this system."""


@cli.group(  # type: ignore[untyped-decorator]
    "precheck",
    short_help="Ensure an OSX Machine Profile is ready to be applied.",
)
def precheck() -> None:
  """Ensure an OSX Machine Profile is ready to be applied."""


@precheck.command("folder")  # type: ignore[untyped-decorator]
@click.argument('folder_path', type=cli_argument_directory)
def check_from_folder(folder_path: str) -> None:
  """Precheck an OSX Machine Profile from a local file system folder.

  FOLDER_PATH: The path to a folder containing a machine profile definition.
  """
  job = jobs.FolderJob(folder_path)
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
@click.argument('spec_file', type=cli_argument_file)
def check_from_spec_file(spec_file: str) -> None:
  """Precheck an OSX Machine Profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file referencing a profile.
  """
  job = jobs.SpecFileJob(spec_file)
  job.precheck()


@apply.command("folder")  # type: ignore[untyped-decorator]
@click.argument('folder_path', type=cli_argument_directory)
def apply_from_folder(folder_path: str) -> None:
  """Apply an OSX Machine Profile from a local file system folder.

  FOLDER_PATH: The path to a folder containing a machine profile definition.
  """
  job = jobs.FolderJob(folder_path)
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
@click.argument('spec_file', type=cli_argument_file)
def apply_from_spec_file(spec_file: str) -> None:
  """Apply an OSX Machine Profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file.
  """
  job = jobs.SpecFileJob(spec_file)
  job.precheck(notes=False)
  job.provision()


@cli.command(  # type: ignore[untyped-decorator]
    "version",
    short_help="Report the current Mac Maker version.",
)
def version() -> None:
  """Report the current Mac Maker version."""
  job = jobs.VersionJob()
  job.invoke()
