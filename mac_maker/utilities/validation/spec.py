"""Job Spec file validator."""

import logging
import os
import pprint
from pathlib import Path
from typing import Any, List, TypedDict, Union

from jsonschema.validators import validator_for
from ... import config
from ..mixins.json_file import JSONFileReader
from ..state import TypeState


class TypeSpecFileData(TypedDict):
  """Typed representation of a loaded Job Spec file."""

  spec_file_content: TypeState
  spec_file_location: Union[Path, str]


class SpecFileValidationException(BaseException):
  """Raised when reading an invalid Job Spec file."""


class SpecFileValidator(JSONFileReader):
  """Validator for a Job Spec file.

  :param spec_file_content: The loaded Job Spec file to validate.
  """

  schema_definition = (
      Path(os.path.dirname(__file__)).parent.parent / "schemas" / "job_v1.json"
  )

  def __init__(self, spec_file_content: TypeState) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.schema = self.load_json_file(self.schema_definition)
    self.spec_file_content = spec_file_content

  def _validate_with_schema(
      self,
      schema: Any,
  ) -> List[str]:
    validator_class = validator_for(schema)
    validator = validator_class(schema)
    errors = []
    for error in validator.iter_errors(self.spec_file_content):
      errors.append(error.message)
    return sorted(errors)

  def validate_spec_file(self) -> None:
    """Validate the loaded Job Spec file.

    :raises: :class:`SpecFileValidationException`
    """

    errors = self._validate_with_schema(self.schema)
    if errors:
      self.log.error('JobSpecValidator: The loaded Job Spec file is invalid!')
      formatted_errors = pprint.pformat(errors)
      raise SpecFileValidationException(formatted_errors)
