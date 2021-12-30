"""Job specification definition."""

import json
import logging
import os
import pprint
from pathlib import Path
from typing import Dict, List, Union

from jsonschema.validators import validator_for
from .. import config
from .filesystem import FileSystem
from .state import State
from .workspace import WorkSpace


class JobSpecFileException(BaseException):
  """Raised when reading an invalid job spec file."""


class JobSpec:
  """Job specification definition."""

  schema_definition = (
      Path(os.path.dirname(__file__)).parent / "schemas" / "job_v1.json"
  )

  def __init__(self):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state_manager = State()
    self.schema = self._load_json_file(self.schema_definition)

  def _load_json_file(self, json_file_location: Union[Path, str]) -> Dict:
    with open(json_file_location, encoding="utf-8") as fhandle:
      json_file_content = json.load(fhandle)
    return json_file_content

  def create_job_spec_from_github(self, workspace: WorkSpace) -> Dict:
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

  def create_job_spec_from_filesystem(
      self,
      spec_file_location: Union[Path, str],
  ) -> Dict:
    """Create (read) a job spec file from the file system.

    :param spec_file_location: The path to the spec file that will be read.
    """

    spec_file_content = self._load_json_file(spec_file_location)
    self._validate_spec_file(spec_file_content)

    return {
        'spec_file_content': spec_file_content,
        'spec_file_location': spec_file_location
    }

  def _validate_with_schema(self, spec_file_content: Dict, schema) -> List:
    validator_class = validator_for(schema)
    validator = validator_class(schema)
    errors = []
    for error in validator.iter_errors(spec_file_content):
      errors.append(error.message)
    return sorted(errors)

  def _validate_spec_file(self, spec_file_content: Dict):
    errors = self._validate_with_schema(spec_file_content, self.schema)
    if errors:
      formatted_errors = pprint.pformat(errors)
      raise JobSpecFileException(formatted_errors)

  def extract_precheck_from_job_spec(
      self,
      spec_file_location: str,
  ) -> Dict[str, str]:
    """Read a profile from a job spec file, and extract the precheck data.

    :param spec_file_location: The path to the spec file that will be read.
    """

    spec_file = self.state_manager.state_rehydrate(Path(spec_file_location))
    workspace_root = Path(spec_file['workspace_root_path'])
    precheck_data = {}

    with open(
        workspace_root / config.PRECHECK['notes'], encoding="utf-8"
    ) as notes_fh:
      precheck_data['notes'] = notes_fh.read()

    with open(
        workspace_root / config.PRECHECK['env'], encoding="utf-8"
    ) as env_fh:
      precheck_data['env'] = env_fh.read()

    return precheck_data
