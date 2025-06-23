"""Extractor for a spec file on the local filesystem."""

import logging
import os
from pathlib import Path
from typing import Union

from mac_maker import config
from mac_maker.profile.spec_file import TypeSpecFileData
from mac_maker.profile.spec_file.spec_file_validator import SpecFileValidator
from mac_maker.utilities.state import State


class SpecFileExtractor:
  """Extractor for a spec file on the local filesystem."""

  schema_definition = (
      Path(os.path.dirname(__file__)).parent / "schemas" / "spec_file_v1.json"
  )

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state_manager = State()

  def get_spec_file_data(
      self,
      spec_file_location: Union[Path, str],
  ) -> TypeSpecFileData:
    """Read a spec file from an arbitrary file system location.

    :param spec_file_location: The path to the spec file that will be read.
    :returns: The loaded spec file.
    """
    self.log.debug('SpecFileExtractor: Reading runtime state from a spec file.')
    spec_file_content = self.state_manager.state_rehydrate(spec_file_location)
    validator = SpecFileValidator(spec_file_content)
    validator.validate_spec_file()
    self.log.debug('SpecFileExtractor: Runtime state has been built.')
    return TypeSpecFileData(
        spec_file_content=spec_file_content,
        spec_file_location=spec_file_location
    )
