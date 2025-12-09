"""Test the Workspace class."""
import logging
import os.path
from logging import Logger
from pathlib import Path
from typing import Callable, Optional
from unittest import mock

import pytest
from mac_maker import config, profile
from mac_maker.__helpers__.logs import decode_logs
from mac_maker.__helpers__.parametrize import templated_ids
from mac_maker.ansible_controller.spec import Spec
from mac_maker.utilities import exceptions, workspace


class TestWorkSpace:
  """Test the Workspace class."""

  vary_branch = pytest.mark.parametrize(
      "branch_name",
      (None, "develop"),
      ids=templated_ids("branch:{0}"),
  )

  vary_folder = pytest.mark.parametrize(
      "folder_path",
      ("/path/folder1", "./relative_path/folder2"),
      ids=templated_ids("folder:{0}"),
  )

  def test_initialize__attributes(
      self,
      workspace_instance: workspace.WorkSpace,
  ) -> None:
    assert isinstance(workspace_instance.log, Logger)
    assert workspace_instance.root == Path(config.WORKSPACE).resolve()
    assert workspace_instance.profile_root is None
    assert workspace_instance.spec_file is None

  def test_initialize__root_exists__removes_existing_workspace_root(
      self,
      mocked_os_module: mock.Mock,
      mocked_shutil_module: mock.Mock,
      setup_workspace_module: Callable[[], None],
  ) -> None:
    setup_workspace_module()
    mocked_os_module.path.exists.return_value = True

    instance = workspace.WorkSpace()

    mocked_os_module.path.exists.assert_called_once_with(instance.root)
    mocked_shutil_module.rmtree.assert_called_once_with(instance.root)

  def test_initialize__no_root_exists__does_not_remove_existing_workspace_root(
      self,
      mocked_os_module: mock.Mock,
      mocked_shutil_module: mock.Mock,
      setup_workspace_module: Callable[[], None],
  ) -> None:
    setup_workspace_module()
    mocked_os_module.path.exists.return_value = False

    instance = workspace.WorkSpace()

    mocked_os_module.path.exists.assert_called_once_with(instance.root)
    mocked_shutil_module.rmtree.assert_not_called()

  @pytest.mark.parametrize(
      "workspace_exists",
      (True, False),
      ids=templated_ids("exists:{0}"),
  )
  def test_initialize__vary_root_exists__creates_workspace_root(
      self,
      mocked_os_module: mock.Mock,
      setup_workspace_module: Callable[[], None],
      workspace_exists: bool,
  ) -> None:
    setup_workspace_module()
    mocked_os_module.path.exists.return_value = workspace_exists

    instance = workspace.WorkSpace()

    mocked_os_module.mkdir.assert_called_once_with(instance.root)

  @vary_folder
  def test_add_folder__vary_folder__successful_copy__copies_folder_to_root(
      self,
      mocked_shutil_module: mock.Mock,
      workspace_instance: workspace.WorkSpace,
      folder_path: str,
  ) -> None:
    workspace_instance.add_folder(folder_path)

    mocked_shutil_module.copytree.assert_called_once_with(
        folder_path,
        workspace_instance.root / os.path.basename(folder_path),
    )

  @vary_folder
  def test_add_folder__vary_folder__failed_copy__raises_correct_exception(
      self,
      mocked_shutil_module: mock.Mock,
      workspace_instance: workspace.WorkSpace,
      folder_path: str,
  ) -> None:
    mocked_shutil_module.copytree.side_effect = Exception

    with pytest.raises(IOError) as exc:
      workspace_instance.add_folder(folder_path)

    assert str(
        exc.value
    ) == (workspace_instance.Messages.error_profile_copy_failure % folder_path)

  @vary_folder
  def test_add_folder__vary_folder__successful_copy__sets_profile_root(
      self,
      workspace_instance: workspace.WorkSpace,
      folder_path: str,
  ) -> None:
    workspace_instance.add_folder(folder_path)

    assert workspace_instance.profile_root == (
        workspace_instance.root / os.path.basename(folder_path)
    )

  @vary_folder
  def test_add_folder__vary_folder__failed_copy__does_not_set_profile_root(
      self,
      mocked_shutil_module: mock.Mock,
      workspace_instance: workspace.WorkSpace,
      folder_path: str,
  ) -> None:
    mocked_shutil_module.copytree.side_effect = Exception

    with pytest.raises(IOError):
      workspace_instance.add_folder(folder_path)

    assert workspace_instance.profile_root is None

  @vary_folder
  def test_add_folder__vary_folder__successful_copy__logging(
      self,
      workspace_instance: workspace.WorkSpace,
      folder_path: str,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    workspace_instance.add_folder(folder_path)

    assert decode_logs(caplog.records) == [
        (
            "DEBUG:mac_maker:" + workspace_instance.Messages.add_folder %
            workspace_instance.profile_root
        ),
    ]

  @vary_folder
  def test_add_folder__vary_folder__failed_copy__no_logging(
      self,
      mocked_shutil_module: mock.Mock,
      workspace_instance: workspace.WorkSpace,
      folder_path: str,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    mocked_shutil_module.copytree.side_effect = Exception
    caplog.set_level(logging.DEBUG)

    with pytest.raises(IOError):
      workspace_instance.add_folder(folder_path)

    assert decode_logs(caplog.records) == []

  @vary_branch
  def test_add_repository__vary_branch__downloads_zip_bundle(
      self,
      mocked_github_repository: mock.Mock,
      workspace_instance: workspace.WorkSpace,
      branch_name: Optional[str],
  ) -> None:
    workspace_instance.add_repository(
        mocked_github_repository,
        branch_name,
    )

    mocked_github_repository \
        .get_zip_bundle_root_folder.assert_called_once_with(branch_name)

  @vary_branch
  def test_add_repository__vary_branch__assigns_profile_root(
      self,
      mocked_github_repository: mock.Mock,
      mocked_profile_root: Path,
      workspace_instance: workspace.WorkSpace,
      branch_name: Optional[str],
  ) -> None:
    workspace_instance.add_repository(
        mocked_github_repository,
        branch_name,
    )

    assert workspace_instance.profile_root == (
        Path(config.WORKSPACE) / mocked_profile_root
    ).resolve()

  @vary_branch
  def test_add_repository__vary_branch__logging(
      self,
      mocked_github_repository: mock.Mock,
      workspace_instance: workspace.WorkSpace,
      branch_name: Optional[str],
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    workspace_instance.add_repository(
        mocked_github_repository,
        branch_name,
    )

    assert decode_logs(caplog.records) == [
        (
            "DEBUG:mac_maker:" + workspace_instance.Messages.add_repository %
            workspace_instance.profile_root
        ),
    ]

  def test_add_spec_file__without_profile__raises_exception(
      self,
      workspace_instance: workspace.WorkSpace,
  ) -> None:
    with pytest.raises(exceptions.WorkSpaceInvalid) as exc:
      workspace_instance.add_spec_file()

    assert str(exc.value) == workspace_instance.Messages.error_no_repository

  def test_add_spec_file__with_profile__creates_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      mocked_spec_file_instance: mock.Mock,
      workspace_instance_with_profile: workspace.WorkSpace,
  ) -> None:
    workspace_instance_with_profile.add_spec_file()

    mocked_spec_file.assert_called_once_with()
    mocked_spec_file_instance.write.assert_called_once_with()

  def test_add_spec_file__with_profile__spec_file_uses_profile_values(
      self,
      mocked_spec_file_instance: mock.Mock,
      workspace_instance_with_profile: workspace.WorkSpace,
  ) -> None:
    assert workspace_instance_with_profile.profile_root is not None
    expected_profile = profile.Profile(
        workspace_instance_with_profile.profile_root
    )

    workspace_instance_with_profile.add_spec_file()

    assert mocked_spec_file_instance.path == \
        expected_profile.get_spec_file()
    assert mocked_spec_file_instance.content == \
        Spec.from_profile(expected_profile)

  def test_add_spec_file__with_profile__logging(
      self,
      workspace_instance_with_profile: workspace.WorkSpace,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    workspace_instance_with_profile.add_spec_file()

    assert decode_logs(caplog.records) == [
        (
            "DEBUG:mac_maker:" +
            workspace_instance_with_profile.Messages.add_spec_file %
            workspace_instance_with_profile.spec_file
        ),
    ]

  def test_add_spec_file__with_profile__updates_spec_file_attribute(
      self,
      workspace_instance_with_profile: workspace.WorkSpace,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    workspace_instance_with_profile.add_spec_file()

    assert isinstance(workspace_instance_with_profile.profile_root, Path)
    assert workspace_instance_with_profile.spec_file == (
        workspace_instance_with_profile.profile_root / "spec.json"
    )
