"""Job specification definition."""

import json
import logging
from pathlib import Path
from typing import Dict

from .. import config
from .filesystem import FileSystem
from .state import State
from .workspace import WorkSpace


class JobSpec:
  """Job specification definition."""

  def __init__(self):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state_manager = State()

  def create_job_spec_from_github(self, workspace: WorkSpace) -> dict:
    """Create a job spec file from a downloaded GitHub based profile.

    :param workspace: The current WorkSpace object in use.
    """

    self.log.debug('JobSpec: Building state from downloaded Git bundle.')
    filesystem = FileSystem(workspace.repository_root)
    spec_file_content = self.state_manager.state_generate(filesystem)

    self.state_manager.state_dehydrate(
        spec_file_content, filesystem.get_spec_file()
    )
    self.log.debug('JobSpec: State has been built.')

    # pylint: disable=unexpected-keyword-arg
    return {
        'spec_file_content': spec_file_content,
        'spec_file_location': filesystem.get_spec_file(string=True)
    }

  def create_job_spec_from_filesystem(self, spec_file_location: str) -> dict:
    """Create (read) a job spec file from the file system.

    :param spec_file_location: The path to the spec file that will be read.
    """

    with open(spec_file_location) as fhandle:
      spec_file_content = json.load(fhandle)
    return {
        'spec_file_content': spec_file_content,
        'spec_file_location': spec_file_location
    }

  def extract_precheck_from_job_spec(
      self,
      spec_file_location: str,
  ) -> Dict[str, str]:
    """Read a profile from a job spec file, and extract the precheck data.

    :param spec_file_location: The path to the spec file that will be read.
    """

    spec_file = self.state_manager.state_rehydrate(Path(spec_file_location))
    workspace_root = Path(spec_file['workspace_root_path'])
    precheck_data = dict()

    with open(workspace_root / config.PRECHECK['notes']) as notes_fh:
      precheck_data['notes'] = notes_fh.read()

    with open(workspace_root / config.PRECHECK['env']) as env_fh:
      precheck_data['env'] = env_fh.read()

    return precheck_data
