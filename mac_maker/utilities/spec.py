"""Job specification definition."""

import json
import logging
import os
import pprint
from pathlib import Path
from typing import Any, List, TypedDict, Union, cast

from jsonschema.validators import validator_for
from .. import config
from .filesystem import FileSystem
from .state import State, TypeState
from .validation.precheck import TypePrecheckFileData
from .workspace import WorkSpace


class TypeSpecFileData(TypedDict):
  """Typed representation of a loaded job spec file."""

  spec_file_content: TypeState
  spec_file_location: Union[Path, str]


class JobSpecFileException(BaseException):
  """Raised when reading an invalid job spec file."""


class JobSpec:
  """Job specification definition."""

  schema_definition = (
      Path(os.path.dirname(__file__)).parent / "schemas" / "job_v1.json"
  )

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state_manager = State()
    self.schema = self._load_json_file(self.schema_definition)

  def _load_json_file(self, json_file_location: Union[Path, str]) -> Any:
    with open(json_file_location, encoding="utf-8") as fhandle:
      json_file_content = json.load(fhandle)
    return json_file_content

  def read_job_spec_from_workspace(
      self, workspace: WorkSpace
  ) -> TypeSpecFileData:
    """Read a job spec file from a created workspace.

    :param workspace: The current WorkSpace object in use.
    :returns: The spec file content, and it's location on the filesystem.
    """

    self.log.debug('JobSpec: Building state from downloaded Git bundle.')
    filesystem = FileSystem(cast(str, workspace.repository_root))
    spec_file_content = self.state_manager.state_generate(filesystem)
    self.state_manager.state_dehydrate(
        spec_file_content, filesystem.get_spec_file()
    )
    self._validate_spec_file(spec_file_content)
    self.log.debug('JobSpec: State has been built.')

    return TypeSpecFileData(
        spec_file_content=spec_file_content,
        spec_file_location=str(filesystem.get_spec_file())
    )

  def read_job_spec_from_filesystem(
      self,
      spec_file_location: Union[Path, str],
  ) -> TypeSpecFileData:
    """Read a job spec file from a arbitrary file system location.

    :param spec_file_location: The path to the spec file that will be read.
    :returns: The spec file content, and it's location on the filesystem.
    """
    spec_file_content = self._load_json_file(spec_file_location)
    self._validate_spec_file(spec_file_content)
    return TypeSpecFileData(
        spec_file_content=spec_file_content,
        spec_file_location=spec_file_location
    )

  def _validate_with_schema(self, spec_file_content: TypeState,
                            schema: Any) -> List[str]:
    validator_class = validator_for(schema)
    validator = validator_class(schema)
    errors = []
    for error in validator.iter_errors(spec_file_content):
      errors.append(error.message)
    return sorted(errors)

  def _validate_spec_file(self, spec_file_content: TypeState) -> None:
    errors = self._validate_with_schema(spec_file_content, self.schema)
    if errors:
      formatted_errors = pprint.pformat(errors)
      raise JobSpecFileException(formatted_errors)

  def extract_precheck_from_job_spec(
      self,
      spec_file_location: str,
  ) -> TypePrecheckFileData:
    """Locate the precheck data from a job spec, and load it.

    :param spec_file_location: The path to the spec file that will be read.
    :returns: The precheck contents.
    """

    spec_file = self.state_manager.state_rehydrate(Path(spec_file_location))
    workspace_root = Path(spec_file['workspace_root_path'])

    with open(
        workspace_root / config.PRECHECK['notes'], encoding="utf-8"
    ) as notes_fh:
      notes = notes_fh.read()

    with open(
        workspace_root / config.PRECHECK['env'], encoding="utf-8"
    ) as env_fh:
      env = env_fh.read()

    return TypePrecheckFileData(
        notes=notes,
        env=env,
    )
