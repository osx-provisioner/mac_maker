"""Test the Profile class."""

from pathlib import Path
from unittest import TestCase

from mac_maker import config
from mac_maker.profile import Profile

MOCK_FOLDER = "mock_folder"


class TestProfile(TestCase):
  """Test the Profile class."""

  def setUp(self) -> None:
    self.mock_root = Path("/root/dir1")
    self.profile = Profile(str(self.mock_root))

  def test_initialize(self) -> None:
    self.assertEqual(
        self.profile.work_space_root,
        self.mock_root,
    )

  def test_get_state_file(self) -> None:
    self.assertEqual(
        self.profile.get_spec_file(), self.mock_root / config.STATE_FILE_NAME
    )

  def test_get_inventory_file(self) -> None:
    self.assertEqual(
        self.profile.get_inventory_file(),
        self.mock_root / config.PROFILE_FOLDER_PATH / "inventory"
    )

  def test_get_galaxy_requirements_file(self) -> None:
    self.assertEqual(
        self.profile.get_galaxy_requirements_file(),
        self.mock_root / config.PROFILE_FOLDER_PATH /
        config.PROFILE_GALAXY_REQUIREMENTS_FILE,
    )

  def test_get_playbook(self) -> None:
    self.assertEqual(
        self.profile.get_playbook_file(),
        self.mock_root / "profile" / config.PROFILE_INSTALLER_FILE
    )

  def test_get_profile_data_path(self) -> None:
    self.assertEqual(
        self.profile.get_profile_data_path(),
        self.mock_root / config.PROFILE_FOLDER_PATH
    )

  def test_get_roles_path(self) -> None:
    self.assertEqual(
        self.profile.get_roles_path(),
        self.mock_root / config.PROFILE_FOLDER_PATH / "roles"
    )

  def test_get_collections_path(self) -> None:
    self.assertEqual(
        self.profile.get_collections_path(),
        self.mock_root / config.PROFILE_FOLDER_PATH / "collections"
    )
