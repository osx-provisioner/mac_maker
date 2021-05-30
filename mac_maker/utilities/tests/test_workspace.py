"""Test the Workspace class."""

from logging import Logger
from pathlib import Path

from parameterized import parameterized
from ... import config
from ...tests.fixtures import fixtures_git
from .. import github, workspace


class TestWorkSpace(fixtures_git.GitTestHarness):
  """Test the Workspace class."""

  def setUp(self):
    super().setUp()
    self.workspace = workspace.WorkSpace()

  def test_init(self):
    self.assertEqual(
        self.workspace.root,
        Path(config.WORKSPACE).resolve(),
    )
    self.assertIsInstance(
        self.workspace.log,
        Logger,
    )

  @parameterized.expand([
      (None,),
      ("develop",),
  ])
  def test_add_repository(self, branch):
    repo = github.GithubRepository(self.repository_http_url)
    self.workspace.add_repository(repo, branch)

    self.assertEqual(
        self.workspace.repository_root,
        self.workspace.root / repo.get_zip_bundle_root_folder(branch)
    )
