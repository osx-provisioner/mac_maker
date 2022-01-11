"""Test the Workspace class."""

from logging import Logger
from pathlib import Path

from ... import config
from ...tests.fixtures import fixtures_git
from .. import github, workspace


class TestWorkSpace(fixtures_git.GitTestHarness):
  """Test the Workspace class."""

  def setUp(self) -> None:
    super().setUp()
    self.workspace = workspace.WorkSpace()

  def test_init(self) -> None:
    self.assertEqual(
        self.workspace.root,
        Path(config.WORKSPACE).resolve(),
    )
    self.assertIsInstance(
        self.workspace.log,
        Logger,
    )

  def test_add_repository_default(self) -> None:
    repo = github.GithubRepository(self.repository_http_url)
    self.workspace.add_repository(repo, None)

    self.assertEqual(
        self.workspace.repository_root,
        self.workspace.root / repo.get_zip_bundle_root_folder(None)
    )

  def test_add_repository_with_name(self) -> None:
    repo = github.GithubRepository(self.repository_http_url)
    self.workspace.add_repository(repo, "branch_name")

    self.assertEqual(
        self.workspace.repository_root,
        self.workspace.root / repo.get_zip_bundle_root_folder("branch_name")
    )
