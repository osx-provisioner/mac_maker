"""Test the SUDO class."""

from unittest import mock

from ... import config
from ...tests.fixtures import fixtures_git
from .. import filesystem, password

PASSWORD_MODULE = password.__name__


class TestSUDO(fixtures_git.GitTestHarness):
  """Test the SUDO password class."""

  def setUp(self):
    super().setUp()
    self.root_folder = "non-existent"
    self.filesystem = filesystem.FileSystem(self.root_folder)
    self.sudo_password = "secret123"
    self.password_helper = password.SUDO(self.filesystem)

  def test_initialize(self):
    self.assertEqual(
        self.password_helper.filesystem,
        self.filesystem,
    )
    self.assertIsNone(self.password_helper.sudo_password)

  @mock.patch(PASSWORD_MODULE + ".getpass.getpass")
  @mock.patch(PASSWORD_MODULE + ".os")
  def test_prompt_for_sudo(self, m_os, m_prompt):
    m_prompt.return_value = "Some Value"

    self.password_helper.prompt_for_sudo()

    self.assertEqual(
        m_prompt.return_value,
        self.password_helper.sudo_password,
    )
    m_prompt.assert_called_once_with(config.SUDO_PROMPT)
    m_os.environ.__setitem__.assert_called_once_with(
        'ANSIBLE_BECOME_PASSWORD', m_prompt.return_value
    )


class TestSUDOEnv(fixtures_git.GitTestHarness):
  """Test the SUDO password class, with environment variables mocked."""

  @mock.patch(
      PASSWORD_MODULE + ".os.environ",
      {config.ENV_ANSIBLE_BECOME_PASSWORD: "already_set"},
  )
  def setUp(self):
    super().setUp()
    self.root_folder = "non-existent"
    self.filesystem = filesystem.FileSystem(self.root_folder)
    self.password_helper = password.SUDO(self.filesystem)

  @mock.patch(PASSWORD_MODULE + ".getpass.getpass")
  def test_prompt_for_sudo_already_set(self, m_prompt):
    self.password_helper.prompt_for_sudo()
    m_prompt.assert_not_called()
    self.assertEqual(self.password_helper.sudo_password, "already_set")
