"""Test the Interpreter class."""

from pathlib import Path
from unittest import TestCase, mock

from mac_maker.ansible_controller import interpreter

INTERPRETER_MODULE = interpreter.__name__


class TestInterpreter(TestCase):
  """Test the Interpreter class."""

  def setUp(self) -> None:
    self.interpreter = interpreter.Interpreter()

  def test_initialize(self) -> None:
    for initialized_interpreter in self.interpreter.options:
      self.assertIsInstance(initialized_interpreter, Path)

  @mock.patch(INTERPRETER_MODULE + ".os")
  def test_first_interpreter_valid(self, m_os: mock.Mock) -> None:

    m_os.path.exists.side_effect = [True]
    self.assertEqual(
        self.interpreter.options[0], self.interpreter.get_interpreter_path()
    )

  @mock.patch(INTERPRETER_MODULE + ".os")
  def test_last_interpreter_valid(self, m_os: mock.Mock) -> None:
    m_os.path.exists.side_effect = [False, True]
    self.assertEqual(
        self.interpreter.options[1], self.interpreter.get_interpreter_path()
    )

  @mock.patch(INTERPRETER_MODULE + ".os")
  def test_no_interpreter_valid(self, m_os: mock.Mock) -> None:
    m_os.path.exists.side_effect = [False, False]
    with self.assertRaises(interpreter.InterpreterNotFound):
      self.interpreter.get_interpreter_path()
