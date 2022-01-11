"""The Mac Maker CLI."""
from typing import Optional

import click
from click_shell import shell
from .jobs import Jobs
from .utilities.logger import Logger


@shell(  # type: ignore[misc]
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


@cli.group("apply")  # type: ignore[misc]
def apply() -> None:
  """Apply an OSX Machine profile to this system."""


@cli.group("precheck")  # type: ignore[misc]
def precheck() -> None:
  """Ensure an OSX machine profile is ready to be applied."""


@precheck.command("github")  # type: ignore[misc]
@click.argument('github_url', type=click.STRING)
@click.option(
    '--branch',
    required=False,
    type=str,
    help="Specific branch (or tag) of the GitHub repo."
)
def check_from_github(github_url: str, branch: Optional[str]) -> None:
  """Precheck a profile from a public GitHub Repository.

  GITHUB_URL: URL of a GitHub repo containing a machine profile definition.
  """
  job = Jobs()
  precheck_data = job.get_precheck_content_from_github(github_url, branch)
  job.precheck(precheck_data)


@precheck.command("spec")  # type: ignore[misc]
@click.argument('spec_file', type=click.STRING)
def check_from_spec(spec_file: str) -> None:
  """Precheck a profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file referencing a profile.
  """
  job = Jobs()
  precheck_data = job.get_precheck_content_from_spec(spec_file)
  job.precheck(precheck_data)


@apply.command("github")  # type: ignore[misc]
@click.argument('github_url', type=click.STRING)
@click.option(
    '--branch',
    required=False,
    type=str,
    help="Specific branch (or tag) of the GitHub repo."
)
def apply_from_github(github_url: str, branch: Optional[str]) -> None:
  """Apply an OSX machine profile from a public GitHub Repository.

  GITHUB_URL: URL of a GitHub repo containing a machine profile definition.
  """
  job = Jobs()
  job_spec = job.create_state_from_github_spec(github_url, branch)
  job.provision(job_spec)


@apply.command("spec")  # type: ignore[misc]
@click.argument('spec_file', type=click.STRING)
def apply_from_spec(spec_file: str) -> None:
  """Apply an OSX machine profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file.
  """
  job = Jobs()
  job_spec = job.create_state_from_local_spec_file(spec_file)
  job.provision(job_spec)


@cli.command("version")  # type: ignore[misc]
def version() -> None:
  """Report the Mac Maker version."""
  job = Jobs()
  job.version()
