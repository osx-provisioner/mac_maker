"""Test the Mac Maker CLI."""

import importlib
from unittest import TestCase, mock

import mac_maker
from click.testing import CliRunner
from mac_maker import cli

ROOT_MODULE = mac_maker.__name__


class TestCommandInterrupt(TestCase):
  """The the command patched_method is patched into the CLI."""

  def setUp(self) -> None:
    self.runner = CliRunner()

  @mock.patch(ROOT_MODULE + ".utilities.shell.cmd_loop.patch_interrupt")
  def test_make_command_interrupt(self, m_interrupt: mock.Mock) -> None:
    importlib.reload(cli)
    cli_root = cli.cli
    original_postcmd = cli_root.shell.postcmd

    with self.assertRaises(SystemExit):
      cli_root(["version"])

    m_interrupt.assert_called_once_with(original_postcmd)
    self.assertEqual(
        cli_root.shell.postcmd,
        m_interrupt.return_value,
    )
