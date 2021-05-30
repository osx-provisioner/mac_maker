"""The Mac Maker CLI."""

import click
from click_shell import shell
from .jobs import Jobs
from .utilities.logger import Logger


@shell(
    prompt='Mac Maker > ',
    intro="Welcome to Mac Maker. (Type 'help' to get started.)",
)
@click.option(
    '--debug', default=False, is_flag=True, help='Enable debug output.'
)
def cli(debug):
  """Mac Maker CLI."""
  logger = Logger(debug=debug)
  logger.setup()


@cli.group("apply")
def apply():
  """Apply an OSX Machine profile to this system."""


@cli.group("precheck")
def precheck():
  """Ensure an OSX machine profile is ready to be applied."""


@precheck.command("github")
@click.argument('github_url', type=click.STRING)
@click.option(
    '--branch',
    required=False,
    type=str,
    help="Specific branch (or tag) of the GitHub repo."
)
def check_from_github(github_url, branch):
  """Precheck a profile from a public GitHub Repository.

  GITHUB_URL: URL of a GitHub repo containing a machine profile definition.
  """
  job = Jobs()
  precheck_data = job.get_precheck_content_from_github(github_url, branch)
  job.precheck(precheck_data)


@precheck.command("spec")
@click.argument('spec_file', type=click.STRING)
def check_from_spec(spec_file):
  """Precheck a profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file referencing a profile.
  """
  job = Jobs()
  precheck_data = job.get_precheck_content_from_spec(spec_file)
  job.precheck(precheck_data)


@apply.command("github")
@click.argument('github_url', type=click.STRING)
@click.option(
    '--branch',
    required=False,
    type=str,
    help="Specific branch (or tag) of the GitHub repo."
)
def apply_from_github(github_url, branch):
  """Apply an OSX machine profile from a public GitHub Repository.

  GITHUB_URL: URL of a GitHub repo containing a machine profile definition.
  """
  job = Jobs()
  job_spec = job.create_spec_from_github(github_url, branch)
  job.provision(job_spec)


@apply.command("spec")
@click.argument('spec_file', type=click.STRING)
def apply_from_spec(spec_file):
  """Apply an OSX machine profile from a spec.json file.

  SPEC_FILE: The location of a spec.json file.
  """
  job = Jobs()
  job_spec = job.create_spec_from_spec_file(spec_file)
  job.provision(job_spec)


@cli.command("version")
def version():
  """Report the Mac Maker version."""
  job = Jobs()
  job.version()
