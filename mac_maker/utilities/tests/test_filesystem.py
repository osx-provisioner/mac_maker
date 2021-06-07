"""Test the Environment class."""

from pathlib import Path
from unittest import TestCase

from ... import config
from .. import filesystem

# pylint: disable=unexpected-keyword-arg

FILESYSTEM_MODULE = filesystem.__name__
MOCK_FOLDER = "mock_folder"


class TestFileSystem(TestCase):
  """Test the FileSystem class."""

  def setUp(self):
    super().setUp()
    self.mock_root = Path("/root/dir1")
    self.filesystem = filesystem.FileSystem(str(self.mock_root))

  def test_initialize(self):
    self.assertEqual(
        self.filesystem.work_space_root,
        self.mock_root,
    )

  def test_get_state_file(self):
    self.assertEqual(
        self.filesystem.get_spec_file(), self.mock_root / config.STATE_FILE_NAME
    )

  def test_get_state_file_str(self):
    self.assertEqual(
        self.filesystem.get_spec_file(string=True),
        str((self.mock_root / config.STATE_FILE_NAME).resolve())
    )

  def test_get_inventory_file(self):
    self.assertEqual(
        self.filesystem.get_inventory_file(),
        self.mock_root / config.PROFILE_FOLDER_PATH / "inventory"
    )

  def test_get_inventory_file_str(self):
    self.assertEqual(
        self.filesystem.get_inventory_file(string=True),
        str(
            (self.mock_root / config.PROFILE_FOLDER_PATH /
             "inventory").resolve()
        )
    )

  def test_get_galaxy_requirements_file(self):
    self.assertEqual(
        self.filesystem.get_galaxy_requirements_file(), self.mock_root /
        config.PROFILE_FOLDER_PATH / config.PROFILE_GALAXY_REQUIREMENTS_FILE
    )

  def test_get_galaxy_requirements_file_str(self):
    expected_path = (
        self.mock_root / config.PROFILE_FOLDER_PATH /
        config.PROFILE_GALAXY_REQUIREMENTS_FILE
    )
    self.assertEqual(
        self.filesystem.get_galaxy_requirements_file(string=True),
        str(expected_path.resolve())
    )

  def test_get_playbook(self):
    self.assertEqual(
        self.filesystem.get_playbook_file(),
        self.mock_root / "profile" / config.PROFILE_INSTALLER_FILE
    )

  def test_get_playbook_str(self):
    self.assertEqual(
        self.filesystem.get_playbook_file(string=True),
        str(
            (self.mock_root / "profile" /
             config.PROFILE_INSTALLER_FILE).resolve()
        )
    )

  def test_get_profile_data_path(self):
    self.assertEqual(
        self.filesystem.get_profile_data_path(),
        self.mock_root / config.PROFILE_FOLDER_PATH
    )

  def test_get_profile_data_path_str(self):
    self.assertEqual(
        self.filesystem.get_profile_data_path(string=True),
        str((self.mock_root / config.PROFILE_FOLDER_PATH).resolve())
    )

  def test_get_roles_path(self):
    self.assertEqual(
        self.filesystem.get_roles_path(),
        self.mock_root / config.PROFILE_FOLDER_PATH / "roles"
    )

  def test_get_roles_path_str(self):
    self.assertEqual(
        self.filesystem.get_roles_path(string=True),
        str((self.mock_root / config.PROFILE_FOLDER_PATH / "roles").resolve())
    )

  def test_get_collections_path(self):
    self.assertEqual(
        self.filesystem.get_collections_path(),
        self.mock_root / config.PROFILE_FOLDER_PATH / "collections"
    )

  def test_get_collections_path_str(self):
    self.assertEqual(
        self.filesystem.get_collections_path(string=True),
        str(
            (self.mock_root / config.PROFILE_FOLDER_PATH /
             "collections").resolve()
        )
    )
