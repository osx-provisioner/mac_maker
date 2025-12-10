"""Test the FolderJob class."""

from typing import Callable
from unittest import mock

import pytest
from mac_maker.__helpers__.parametrize import templated_ids
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.jobs.folder import FolderJob


class TestFolderJob:
  """Test the FolderJob class."""

  vary_folder = pytest.mark.parametrize(
      "folder_path",
      ("/path/folder1", "./relative_path/folder2"),
      ids=templated_ids("folder:{0}"),
  )

  @vary_folder
  def test_initialize__vary_path__has_correct_inheritance(
      self,
      folder_path: str,
  ) -> None:
    instance = FolderJob(folder_path)

    assert isinstance(instance, FolderJob)
    assert isinstance(instance, ProvisionerJobBase)

  @vary_folder
  def test_initialize__vary_path__has_correct_attributes(
      self,
      folder_path: str,
  ) -> None:
    instance = FolderJob(folder_path)

    assert instance.folder_path == folder_path
    assert instance.workspace is None

  def test_initialize_spec_file__calls_echo(
      self,
      mocked_click_echo: mock.Mock,
      folder_job_instance: FolderJob,
  ) -> None:
    folder_job_instance.initialize_spec_file()

    mocked_click_echo.assert_called_once_with(
        folder_job_instance.Messages.load_folder_profile
    )

  @vary_folder
  def test_initialize_spec_file__vary_folder__creates_workspace(
      self,
      mocked_workspace: mock.Mock,
      setup_folder_job_module: Callable[[], None],
      folder_path: str,
  ) -> None:
    setup_folder_job_module()
    instance = FolderJob(folder_path)

    instance.initialize_spec_file()

    mocked_workspace.assert_called_once_with()
    assert instance.workspace == mocked_workspace.return_value

  @vary_folder
  def test_initialize_spec_file__vary_folder__adds_folder_to_workspace(
      self,
      mocked_workspace: mock.Mock,
      setup_folder_job_module: Callable[[], None],
      folder_path: str,
  ) -> None:
    setup_folder_job_module()
    instance = FolderJob(folder_path)

    instance.initialize_spec_file()

    mocked_workspace.return_value.add_folder.assert_called_once_with(
        folder_path
    )

  @vary_folder
  def test_initialize_spec_file__vary_folder__adds_spec_file_to_workspace(
      self,
      mocked_workspace: mock.Mock,
      setup_folder_job_module: Callable[[], None],
      folder_path: str,
  ) -> None:
    setup_folder_job_module()
    instance = FolderJob(folder_path)

    instance.initialize_spec_file()

    mocked_workspace.return_value.add_spec_file.assert_called_once_with()

  @vary_folder
  def test_initialize_spec_file__vary_folder__initializes_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      setup_folder_job_module: Callable[[], None],
      folder_path: str,
  ) -> None:
    setup_folder_job_module()
    instance = FolderJob(folder_path)

    instance.initialize_spec_file()

    assert instance.workspace is not None
    assert mocked_spec_file.return_value.path == \
        str(instance.workspace.spec_file)

  @vary_folder
  def test_initialize_spec_file__vary_folder__loads_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      setup_folder_job_module: Callable[[], None],
      folder_path: str,
  ) -> None:
    setup_folder_job_module()
    instance = FolderJob(folder_path)

    instance.initialize_spec_file()

    mocked_spec_file.return_value.load.assert_called_once_with()
