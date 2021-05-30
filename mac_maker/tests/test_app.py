"""Test the Default App"""

from io import StringIO
from unittest import TestCase, mock

from ..app import main


class AppTest(TestCase):

  def test_app_stdout(self):
    with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
      main()
      self.assertEqual(mock_stdout.getvalue(), "Hello World!")
