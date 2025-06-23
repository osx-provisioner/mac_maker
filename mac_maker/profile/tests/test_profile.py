"""Test the Profile class."""

from pathlib import Path

from mac_maker import config
from mac_maker.profile import Profile

MOCK_FOLDER = "mock_folder"


class TestProfile:
  """Test the Profile class."""

  def test_initialize__attributes(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.profile_root == mocked_profile_root

  def test_get_spec_file__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_spec_file(
    ) == (mocked_profile_root / config.SPEC_FILE_NAME)

  def test_get_inventory_file__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_inventory_file() == (
        mocked_profile_root / config.PROFILE_FOLDER_PATH /
        config.PROFILE_INVENTORY_FILE
    )

  def test_get_galaxy_requirements_file__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_galaxy_requirements_file() == (
        mocked_profile_root / config.PROFILE_FOLDER_PATH /
        config.PROFILE_GALAXY_REQUIREMENTS_FILE
    )

  def test_get_playbook_file__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_playbook_file() == (
        mocked_profile_root / config.PROFILE_FOLDER_PATH /
        config.PROFILE_INSTALLER_FILE
    )

  def test_get_profile_data_path__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_profile_data_path(
    ) == (mocked_profile_root / config.PROFILE_FOLDER_PATH)

  def test_get_roles_path__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_roles_path(
    ) == (mocked_profile_root / config.PROFILE_FOLDER_PATH / "roles")

  def test_get_collections_path__returns_correct_value(
      self,
      mocked_profile_root: Path,
      profile_instance: Profile,
  ) -> None:
    assert profile_instance.get_collections_path(
    ) == (mocked_profile_root / config.PROFILE_FOLDER_PATH / "collections")
