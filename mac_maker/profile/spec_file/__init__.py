"""A file containing an Ansible provisioning specification."""

import logging
from dataclasses import asdict
from pathlib import Path
from typing import Optional, Union

from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile.spec_file.exceptions import (
    SpecFileContentNotDefined,
    SpecFilePathNotDefined,
)
from mac_maker.profile.spec_file.spec_file_validator import SpecFileValidator
from mac_maker.utilities.mixins.json_file import JSONFileReader, JSONFileWriter


class SpecFile(JSONFileReader, JSONFileWriter):
  """A file containing an Ansible provisioning specification."""

  class Messages:
    generate_start = "SpecFile: Generating spec file content ..."
    generate_end = "SpecFile: spec file content generated successfully!"
    load_start = "SpecFile: Loading spec content ..."
    load_end = "SpecFile: '%s' loaded successfully!"
    write_start = "SpecFile: Saving spec content ..."
    write_end = "SpecFile: '%s' saved successfully!"

  _content: Optional[Spec]
  _path: Union[Path, str, None]

  def __init__(self) -> None:
    self._content = None
    self._path = None
    self.log = logging.getLogger(config.LOGGER_NAME)

  @property
  def content(self) -> Spec:
    """Return the spec file's content.

    :returns: The spec file content.
    :raises: :class:`SpecFileContentNotDefined`
    """
    if not self._content:
      raise SpecFileContentNotDefined

    return self._content

  @content.setter
  def content(self, spec: Spec) -> None:
    """Assigns the spec file's content.

    :spec: The spec file content.
    """

    self._content = spec

  @property
  def path(self) -> Union[Path, str]:
    """Return the path to the spec file.

    :returns: The path to the spec file.
    :raises: :class:`SpecFilePathNotDefined`
    """

    if not self._path:
      raise SpecFilePathNotDefined

    return self._path

  @path.setter
  def path(self, path: Union[Path, str]) -> None:
    """Assigns the spec file's path.

    :spec: The path to the spec file.
    """

    self._path = path

  def load(self) -> None:
    """Read a spec object from a file on the file system."""

    self.log.debug(self.Messages.load_start)

    json_content = self.load_json_file(self.path)

    validator = SpecFileValidator(json_content)
    validator.validate()

    self.content = Spec(**json_content)

    self.log.debug(self.Messages.load_end, self.path)

  def write(self) -> None:
    """Save a spec object to file on the file system."""

    self.log.debug(self.Messages.write_start)

    self.write_json_file(asdict(self.content), self.path)

    self.log.debug(self.Messages.write_end, self.path)
