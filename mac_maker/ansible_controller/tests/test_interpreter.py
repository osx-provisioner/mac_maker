"""Test the AnsibleInterpreter class."""

from pathlib import Path
from typing import Tuple
from unittest import mock

import pytest
from mac_maker.__helpers__.parametrize import named_parameters
from mac_maker.ansible_controller import exceptions, interpreter

INTERPRETER_MODULE = interpreter.__name__


class TestAnsibleInterpreter:
  """Test the AnsibleInterpreter class."""

  def test_initialize__attributes(
      self,
      ansible_interpreter: interpreter.AnsibleInterpreter,
  ) -> None:
    assert ansible_interpreter.options == [
        Path("/usr/bin/python"),
        Path("/usr/bin/python3"),
    ]

  @pytest.mark.parametrize(
      "exists_return_sequence,expected_path",
      named_parameters(
          (
              (True,),
              interpreter.AnsibleInterpreter.options[0],
          ),
          (
              (False, True),
              interpreter.AnsibleInterpreter.options[1],
          ),
          names=[1],
      ),
  )
  def test_get_interpreter_path__vary_available__returns_correct_path(
      self,
      ansible_interpreter: interpreter.AnsibleInterpreter,
      mocked_os: mock.Mock,
      exists_return_sequence: Tuple[bool, ...],
      expected_path: Path,
  ) -> None:
    mocked_os.path.exists.side_effect = exists_return_sequence

    result = ansible_interpreter.get_interpreter_path()

    assert result == expected_path

  def test_get_interpreter_path__not_available__returns_correct_path(
      self,
      ansible_interpreter: interpreter.AnsibleInterpreter,
      mocked_os: mock.Mock,
  ) -> None:
    mocked_os.path.exists.side_effect = \
        (False,) * len(ansible_interpreter.options)

    with pytest.raises(exceptions.AnsibleInterpreterNotFound):
      ansible_interpreter.get_interpreter_path()
