"""A file containing an Ansible provisioning specification."""

import logging
from mac_maker import config
from pathlib import Path
from mac_maker.ansible_controller.spec import Spec
from typing import Union, Optional
from mac_maker.profile.spec_file.exceptions import SpecFileValidationException, SpecFileNotDefined
from mac_maker.utilities.mixins.json_file import JSONFileReader, JSONFileWriter
from mac_maker.profile.spec_file.spec_file_validator import SpecFileValidator
from mac_maker.profile import Profile


class SpecFile(JSONFileReader, JSONFileWriter):
  """A file containing an Ansible provisioning specification."""

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
    :raises: :class:`SpecFileNotDefined`
    """
    if not self._content:
      raise SpecFileNotDefined

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
    :raises: :class:`SpecFileNotDefined`
    """

    if not self._path:
      raise SpecFileNotDefined

    return self._path

  @path.setter
  def path(self, path: Union[Path, str]) -> None:
    """Assigns the spec file's path.

    :spec: The path to the spec file.
    """

    self._path = path

  def generate(self, profile: Profile) -> None:
    """Generate spec file content from a profile instance.

    :param profile: The profile being used.
    """

    self.log.debug("SpecFile: Generating spec file content ...")

    self.content = Spec(
      workspace_root_path=str(profile.get_work_space_root().resolve()),
      profile_data_path=str(profile.get_profile_data_path().resolve()),
      galaxy_requirements_file=str(
        profile.get_galaxy_requirements_file().resolve()
      ),
      playbook=str(profile.get_playbook_file().resolve()),
      roles_path=[str(profile.get_roles_path().resolve())],
      collections_path=[str(profile.get_collections_path().resolve())],
      inventory=str(profile.get_inventory_file().resolve()),
    )

  def load(
      self,
      spec_file_path: Union[Path, str],
  ) -> None:
    """Read a spec object from a file on the file system.

    :param spec_file_path: The path to the spec file that will be read.
    :raises: :class:`SpecFileValidationException`, :class:`SpecFileNotDefined`
    """

    self.log.debug("SpecFile: Loading spec content ...")

    content = self.load_json_file(spec_file_path)

    validator = SpecFileValidator(content)
    validator.validate_spec_file()

    self._content = Spec(**content)
    self._path = self._path

  def save(
      self,
      spec_file_path: Union[Path, str],
  ) -> None:
    """Save a spec object to file on the file system.

    :param spec_file_path: The path to the spec file that will be written.
    :raises: :class:`SpecFileNotDefined`
    """

    if not self._content:
      raise SpecFileNotDefined

    self.log.debug("SpecFile: Saving spec content ...")

    self.write_json_file(self.content, spec_file_path)
    self._path = self._path
