"""Test the InventoryFile class."""

from logging import Logger
from pathlib import Path
from unittest import TestCase, mock

from mac_maker import config
from mac_maker.ansible_controller import interpreter, inventory
from mac_maker.profile import Profile
from mac_maker.utilities import state

INVENTORY_MODULE = inventory.__name__


class TestInventoryFile(TestCase):
  """Test the InventoryFile class."""

  def setUp(self) -> None:
    self.root_folder = "/root/mock/dir1"
    self.profile = Profile(self.root_folder)
    self.state = state.State()
    self.loaded_state = self.state.state_generate(self.profile)
    self.inventory = inventory.InventoryFile(self.loaded_state)

  def test_initialize(self) -> None:
    self.assertIsInstance(
        self.inventory.log,
        Logger,
    )
    self.assertEqual(self.inventory.state, self.loaded_state)
    self.assertIsInstance(self.inventory.interpreter, interpreter.Interpreter)

  @mock.patch(INVENTORY_MODULE + ".os")
  @mock.patch(INVENTORY_MODULE + ".TextFileWriter.write_text_file")
  @mock.patch(INVENTORY_MODULE + ".Interpreter.get_interpreter_path")
  def test_write_inventory_file(
      self, m_interpreter: mock.Mock, m_write: mock.Mock, m_os: mock.Mock
  ) -> None:

    m_os.path.exists.return_value = False
    m_interpreter.return_value = Path("/usr/bin/mock")

    self.inventory.write_inventory_file()

    m_os.makedirs.assert_called_once_with(
        self.loaded_state['profile_data_path'],
        exist_ok=True,
    )

    expected_inventory = config.ANSIBLE_INVENTORY_CONTENT

    expected_inventory += "ansible_python_interpreter="
    expected_inventory += str(m_interpreter.return_value)
    expected_inventory += "\n"

    m_write.assert_called_once_with(
        expected_inventory, self.loaded_state['inventory']
    )

  @mock.patch(INVENTORY_MODULE + ".os")
  @mock.patch(INVENTORY_MODULE + ".TextFileWriter.write_text_file")
  def test_write_inventory_file_already_exists(
      self, m_write: mock.Mock, m_os: mock.Mock
  ) -> None:
    m_os.path.exists.return_value = True

    self.inventory.write_inventory_file()

    m_os.makedirs.assert_not_called()
    m_write.assert_not_called()
