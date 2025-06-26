"""Test the SUDO class."""

from unittest import mock

from mac_maker import config
from mac_maker.tests.fixtures import fixtures_git
from mac_maker.utilities import sudo

SUDO_MODULE = sudo.__name__


class MockPopenResponse:
  """Mock :class:`subprocess.Popen` response."""

  def __init__(self, returncode: int) -> None:
    self.returncode = returncode
    self.communicate = mock.Mock()


class TestSUDO(fixtures_git.GitTestHarness):
  """Test the SUDO password class."""

  def setUp(self) -> None:
    super().setUp()
    self.sudo_password = "secret123"
    self.password_helper = sudo.SUDO()

    self.successful_sudo = MockPopenResponse(0)
    self.unsuccessful_sudo = MockPopenResponse(1)

  def test_initialize(self) -> None:
    self.assertIsNone(self.password_helper.sudo_password)

  @mock.patch(SUDO_MODULE + ".getpass.getpass")
  @mock.patch(SUDO_MODULE + ".os")
  @mock.patch(SUDO_MODULE + ".subprocess.Popen")
  def test_prompt_for_sudo(
      self, m_p_open: mock.Mock, m_os: mock.Mock, m_prompt: mock.Mock
  ) -> None:

    m_p_open.return_value.__enter__.side_effect = [
        self.unsuccessful_sudo,
        self.successful_sudo,
    ]

    m_prompt.return_value = "Some Value"

    self.password_helper.prompt_for_sudo()

    self.assertEqual(
        m_prompt.return_value,
        self.password_helper.sudo_password,
    )
    m_prompt.call_list = [
        mock.call(config.SUDO_PROMPT),
        mock.call(config.SUDO_PROMPT),
    ]

    m_os.environ.__setitem__.assert_called_once_with(
        'ANSIBLE_BECOME_PASSWORD', m_prompt.return_value
    )


class TestSUDOEnv(fixtures_git.GitTestHarness):
  """Test the SUDO password class, with environment variables mocked."""

  @mock.patch(
      SUDO_MODULE + ".os.environ",
      {config.ENV_ANSIBLE_BECOME_PASSWORD: "already_set"},
  )
  def setUp(self) -> None:
    super().setUp()
    self.password_helper = sudo.SUDO()

  @mock.patch(SUDO_MODULE + ".getpass.getpass")
  def test_prompt_for_sudo_already_set(self, m_prompt: mock.Mock) -> None:
    self.password_helper.prompt_for_sudo()
    m_prompt.assert_not_called()
    self.assertEqual(self.password_helper.sudo_password, "already_set")
