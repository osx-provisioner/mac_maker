"""Extractor for Job Spec files on the local filesystem."""

import logging
import os
from pathlib import Path
from typing import TypedDict, Union

from .. import config
from .state import State, TypeState
from .validation.spec import SpecFileValidator


class TypeSpecFileData(TypedDict):
  """Typed representation of a loaded Job Spec file."""

  spec_file_content: TypeState
  spec_file_location: Union[Path, str]


class JobSpecExtractor:
  """Extractor for Job Spec files on the local filesystem."""

  schema_definition = (
      Path(os.path.dirname(__file__)).parent / "schemas" / "job_v1.json"
  )

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state_manager = State()

  def get_job_spec_data(
      self,
      spec_file_location: Union[Path, str],
  ) -> TypeSpecFileData:
    """Read a Job Spec file from an arbitrary file system location.

    :param spec_file_location: The path to the Job Spec file that will be read.
    :returns: The Job Spec file contents, and it's location on the filesystem.
    """
    self.log.debug(
        'JobSpecExtractor: Reading runtime state from a Job Spec file.'
    )
    spec_file_content = self.state_manager.state_rehydrate(spec_file_location)
    validator = SpecFileValidator(spec_file_content)
    validator.validate_spec_file()
    self.log.debug('JobSpecExtractor: Runtime state has been built.')
    return TypeSpecFileData(
        spec_file_content=spec_file_content,
        spec_file_location=spec_file_location
    )
