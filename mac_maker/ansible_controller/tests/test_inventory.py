"""Test the AnsibleInventoryFile class."""

from logging import Logger
from unittest import mock

from mac_maker import config
from mac_maker.ansible_controller import inventory, spec


class TestAnsibleInventoryFile:
  """Test the AnsibleInventoryFile class."""

  def test_initialize__attributes(
      self,
      ansible_inventory: inventory.AnsibleInventoryFile,
      global_spec_mock: spec.Spec,
  ) -> None:
    assert isinstance(ansible_inventory.log, Logger)
    assert ansible_inventory.spec == global_spec_mock

  def test_initialize__creates_interpreter(
      self,
      ansible_inventory: inventory.AnsibleInventoryFile,
      mocked_ansible_interpreter: mock.Mock,
  ) -> None:
    mocked_ansible_interpreter.assert_called_once_with()
    assert ansible_inventory.interpreter == \
        mocked_ansible_interpreter.return_value

  def test_write__non_existing__creates_directories(
      self,
      ansible_inventory: inventory.AnsibleInventoryFile,
      mocked_os: mock.Mock,
      mocked_ansible_interpreter_instance: mock.Mock,
  ) -> None:
    mocked_os.path.exists.return_value = False
    mocked_ansible_interpreter_instance.get_interpreter_path.return_value = \
        "/mock/path"

    ansible_inventory.write()

    mocked_os.makedirs.assert_called_once_with(
        ansible_inventory.spec.profile_data_path,
        exist_ok=True,
    )

  def test_write__non_existing__writes_file(
      self,
      ansible_inventory: inventory.AnsibleInventoryFile,
      mocked_os: mock.Mock,
      mocked_ansible_interpreter_instance: mock.Mock,
      mocked_textfile_write: mock.Mock,
  ) -> None:
    mocked_os.path.exists.return_value = False
    mocked_ansible_interpreter_instance.get_interpreter_path.return_value = \
        "/mock/path"
    expected_inventory = config.ANSIBLE_INVENTORY_CONTENT
    expected_inventory += "ansible_python_interpreter="
    expected_inventory += (
        mocked_ansible_interpreter_instance.get_interpreter_path.return_value
    )
    expected_inventory += "\n"

    ansible_inventory.write()

    mocked_textfile_write.assert_called_once_with(
        expected_inventory,
        ansible_inventory.spec.inventory,
    )

  def test_write__existing__does_not_create_directories(
      self,
      ansible_inventory: inventory.AnsibleInventoryFile,
      mocked_os: mock.Mock,
      mocked_ansible_interpreter_instance: mock.Mock,
  ) -> None:
    mocked_os.path.exists.return_value = True
    mocked_ansible_interpreter_instance.get_interpreter_path.return_value = \
        "/mock/path"

    ansible_inventory.write()

    mocked_os.makedirs.assert_not_called()

  def test_write__existing__does_not_write_file(
      self,
      ansible_inventory: inventory.AnsibleInventoryFile,
      mocked_os: mock.Mock,
      mocked_ansible_interpreter_instance: mock.Mock,
      mocked_textfile_write: mock.Mock,
  ) -> None:
    mocked_os.path.exists.return_value = True
    mocked_ansible_interpreter_instance.get_interpreter_path.return_value = \
        "/mock/path"

    ansible_inventory.write()

    mocked_textfile_write.assert_not_called()
