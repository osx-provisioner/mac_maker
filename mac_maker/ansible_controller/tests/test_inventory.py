"""Test the InventoryFile class."""

from logging import Logger
from unittest import TestCase, mock

from ... import config
from ...utilities import filesystem, state
from .. import inventory

INVENTORY_MODULE = inventory.__name__


class TestInventoryFile(TestCase):
  """Test the InventoryFile class."""

  def setUp(self) -> None:
    super().setUp()
    self.root_folder = "/root/mock/dir1"
    self.filesystem = filesystem.FileSystem(self.root_folder)
    self.state = state.State()
    self.loaded_state = self.state.state_generate(self.filesystem)
    self.inventory = inventory.InventoryFile(self.loaded_state)

  def test_initialize(self) -> None:
    self.assertIsInstance(
        self.inventory.log,
        Logger,
    )
    self.assertEqual(self.inventory.state, self.loaded_state)

  @mock.patch(INVENTORY_MODULE + ".os")
  @mock.patch("builtins.open", new_callable=mock.mock_open)
  def test_write_inventory_file(
      self, m_open: mock.Mock, m_os: mock.Mock
  ) -> None:

    m_os.path.exists.return_value = False

    self.inventory.write_inventory_file()

    m_os.makedirs.assert_called_once_with(
        self.loaded_state['profile_data_path'],
        exist_ok=True,
    )

    m_open.assert_called_once_with(
        self.loaded_state['inventory'], 'w', encoding="utf-8"
    )
    handle = m_open()
    handle.write.assert_called_once_with(config.ANSIBLE_INVENTORY_CONTENT)

  @mock.patch(INVENTORY_MODULE + ".os")
  @mock.patch("builtins.open", new_callable=mock.mock_open)
  def test_write_inventory_file_already_exists(
      self, m_open: mock.Mock, m_os: mock.Mock
  ) -> None:
    m_os.path.exists.return_value = True

    self.inventory.write_inventory_file()

    m_os.makedirs.assert_not_called()
    m_open.assert_not_called()
