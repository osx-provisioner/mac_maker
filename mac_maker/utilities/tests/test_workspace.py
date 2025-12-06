"""Test the Workspace class."""
import logging
from logging import Logger
from pathlib import Path
from typing import Optional
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

  def test_initialize__attributes(
      self,
      workspace_instance: workspace.WorkSpace,
  ) -> None:
    assert isinstance(workspace_instance.log, Logger)
    assert workspace_instance.root == Path(config.WORKSPACE).resolve()
    assert workspace_instance.repository_root is None
    assert workspace_instance.spec_file is None

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
  def test_add_repository__vary_branch__assigns_repository_root(
      self,
      mocked_github_repository: mock.Mock,
      mocked_repository_root: Path,
      workspace_instance: workspace.WorkSpace,
      branch_name: Optional[str],
  ) -> None:
    workspace_instance.add_repository(
        mocked_github_repository,
        branch_name,
    )

    assert workspace_instance.repository_root == (
        Path(config.WORKSPACE) / mocked_repository_root
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
            workspace_instance.repository_root
        ),
    ]

  def test_add_spec_file__without_repository__raises_exception(
      self,
      workspace_instance: workspace.WorkSpace,
  ) -> None:
    with pytest.raises(exceptions.WorkSpaceInvalid) as exc:
      workspace_instance.add_spec_file()

    assert str(exc.value) == workspace_instance.Messages.error_no_repository

  def test_add_spec_file__with_repository__creates_spec_file(
      self,
      mocked_spec_file: mock.Mock,
      mocked_spec_file_instance: mock.Mock,
      workspace_instance_with_repository: workspace.WorkSpace,
  ) -> None:
    workspace_instance_with_repository.add_spec_file()

    mocked_spec_file.assert_called_once_with()
    mocked_spec_file_instance.write.assert_called_once_with()

  def test_add_spec_file__with_repository__spec_file_uses_profile_values(
      self,
      mocked_spec_file_instance: mock.Mock,
      workspace_instance_with_repository: workspace.WorkSpace,
  ) -> None:
    assert workspace_instance_with_repository.repository_root is not None
    expected_profile = profile.Profile(
        workspace_instance_with_repository.repository_root
    )

    workspace_instance_with_repository.add_spec_file()

    assert mocked_spec_file_instance.path == \
        expected_profile.get_spec_file()
    assert mocked_spec_file_instance.content == \
        Spec.from_profile(expected_profile)

  def test_add_spec_file__with_repository__logging(
      self,
      workspace_instance_with_repository: workspace.WorkSpace,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    workspace_instance_with_repository.add_spec_file()

    assert decode_logs(caplog.records) == [
        (
            "DEBUG:mac_maker:" +
            workspace_instance_with_repository.Messages.add_spec_file %
            workspace_instance_with_repository.spec_file
        ),
    ]

  def test_add_spec_file__with_repository__updates_spec_file_attribute(
      self,
      workspace_instance_with_repository: workspace.WorkSpace,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)

    workspace_instance_with_repository.add_spec_file()

    assert isinstance(workspace_instance_with_repository.repository_root, Path)
    assert workspace_instance_with_repository.spec_file == (
        workspace_instance_with_repository.repository_root / "spec.json"
    )
