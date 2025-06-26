"""Test the Workspace class."""

from logging import Logger
from pathlib import Path
from unittest import mock

from mac_maker import config
from mac_maker.tests.fixtures import fixtures_git
from mac_maker.utilities import github, workspace

WORKSPACE_MODULE = workspace.__name__


class TestWorkSpace(fixtures_git.GitTestHarness):
  """Test the Workspace class."""

  def setUp(self) -> None:
    super().setUp()
    self.mock_temp_directory = "/mock_temp_directory"
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
    self.assertIsNone(self.workspace.repository_root,)
    self.assertIsNone(self.workspace.spec_file,)

  @mock.patch(
      WORKSPACE_MODULE + ".GithubRepository.download_zip_bundle_profile"
  )
  def test_add_repository_default(self, m_download: mock.Mock) -> None:
    branch_name = None
    repo = github.GithubRepository(self.repository_http_url)
    self.workspace.add_repository(repo, branch_name)

    self.assertEqual(
        self.workspace.repository_root,
        self.workspace.root / repo.get_zip_bundle_root_folder(branch_name)
    )
    m_download.assert_called_once_with(self.workspace.root, branch_name)

  @mock.patch(
      WORKSPACE_MODULE + ".GithubRepository.download_zip_bundle_profile"
  )
  def test_add_repository_with_name(self, m_download: mock.Mock) -> None:
    branch_name = "mock_branch_name"
    repo = github.GithubRepository(self.repository_http_url)
    self.workspace.add_repository(repo, branch_name)

    self.assertEqual(
        self.workspace.repository_root,
        self.workspace.root / repo.get_zip_bundle_root_folder(branch_name)
    )
    m_download.assert_called_once_with(self.workspace.root, branch_name)

  def test_add_spec_file_no_repo(self) -> None:
    with self.assertRaises(workspace.InvalidWorkspace):
      self.workspace.add_spec_file()
    self.assertIsNone(self.workspace.spec_file)

  @mock.patch(WORKSPACE_MODULE + ".State")
  @mock.patch(WORKSPACE_MODULE + ".FileSystem")
  def test_add_spec_file_with_repo(
      self, m_fs: mock.Mock, m_state: mock.Mock
  ) -> None:
    mock_spec_file_path = "/mock/path"
    mock_spec_file_content = "mock state"

    m_fs.return_value.get_spec_file.return_value = mock_spec_file_path
    m_state.return_value.state_generate.return_value = mock_spec_file_content

    self.workspace.repository_root = Path("/mock_root_path")
    self.workspace.add_spec_file()

    m_state.return_value.state_dehydrate.assert_called_once_with(
        mock_spec_file_content, mock_spec_file_path
    )
    self.assertEqual(self.workspace.spec_file, mock_spec_file_path)
