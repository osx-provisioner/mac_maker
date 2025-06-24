"""Test the SpecFile class."""

import logging
from dataclasses import asdict
from typing import NamedTuple, Type
from unittest import mock

import pytest
from mac_maker.__helpers__.logs import decode_logs
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile.spec_file import SpecFile, exceptions


class TestSpecFile:
  """Test the SpecFile class."""

  def test_initializer__logger(
      self,
      spec_file_instance: SpecFile,
  ) -> None:
    assert isinstance(spec_file_instance.log, logging.Logger)

  def test_content__set__returns_correct_value(
      self,
      global_spec_mock: Spec,
      spec_file_instance: SpecFile,
  ) -> None:
    spec_file_instance.content = global_spec_mock

    result = spec_file_instance.content

    assert result == global_spec_mock

  def test_content__unset__raises_exception(
      self,
      spec_file_instance: SpecFile,
  ) -> None:
    with pytest.raises(exceptions.SpecFileContentNotDefined):
      _ = spec_file_instance.content

  def test_path__set__returns_correct_value(
      self,
      global_spec_file_path_mock: str,
      spec_file_instance: SpecFile,
  ) -> None:
    spec_file_instance.path = global_spec_file_path_mock

    result = spec_file_instance.path

    assert result == global_spec_file_path_mock

  def test_path__unset__raises_exception(
      self,
      spec_file_instance: SpecFile,
  ) -> None:
    with pytest.raises(exceptions.SpecFilePathNotDefined):
      _ = spec_file_instance.path

  def test_load__path_set__reads_json_file(
      self,
      global_spec_file_path_mock: str,
      mocked_jsonfile_read: mock.Mock,
      spec_file_instance: SpecFile,
  ) -> None:
    spec_file_instance.path = global_spec_file_path_mock

    spec_file_instance.load()

    mocked_jsonfile_read.assert_called_once_with(global_spec_file_path_mock)

  def test_load__path_set__validates_json_content(
      self,
      global_spec_file_path_mock: str,
      mocked_jsonfile_read: mock.Mock,
      mocked_spec_file_validator: mock.Mock,
      spec_file_instance: SpecFile,
  ) -> None:
    spec_file_instance.path = global_spec_file_path_mock

    spec_file_instance.load()

    mocked_spec_file_validator.assert_called_once_with(
        mocked_jsonfile_read.return_value
    )
    mocked_spec_file_validator \
        .return_value.validate.assert_called_once_with()

  def test_load__path_set__assigns_spec_content(
      self,
      global_spec_file_path_mock: str,
      global_spec_mock: Spec,
      spec_file_instance: SpecFile,
  ) -> None:
    spec_file_instance.path = global_spec_file_path_mock

    spec_file_instance.load()

    assert spec_file_instance.content == global_spec_mock

  def test_load__path_set__logging(
      self,
      global_spec_file_path_mock: str,
      spec_file_instance: SpecFile,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)
    spec_file_instance.path = global_spec_file_path_mock

    spec_file_instance.load()

    assert decode_logs(caplog.records) == [
        f"DEBUG:mac_maker:{spec_file_instance.Messages.load_start}",
        (
            "DEBUG:mac_maker:" +
            spec_file_instance.Messages.load_end % spec_file_instance.path
        ),
    ]

  def test_load__path_unset__raises_exception(
      self,
      spec_file_instance: SpecFile,
  ) -> None:
    with pytest.raises(exceptions.SpecFilePathNotDefined):
      spec_file_instance.load()

  def test_write__path_set__content_set__writes_json_file(
      self,
      global_spec_file_path_mock: str,
      global_spec_mock: Spec,
      mocked_jsonfile_write: mock.Mock,
      spec_file_instance: SpecFile,
  ) -> None:
    spec_file_instance.path = global_spec_file_path_mock
    spec_file_instance.content = global_spec_mock

    spec_file_instance.write()

    mocked_jsonfile_write.assert_called_once_with(
        asdict(global_spec_mock),
        global_spec_file_path_mock,
    )

  def test_write__path_set__content_set__logging(
      self,
      global_spec_file_path_mock: str,
      global_spec_mock: Spec,
      spec_file_instance: SpecFile,
      caplog: pytest.LogCaptureFixture,
  ) -> None:
    caplog.set_level(logging.DEBUG)
    spec_file_instance.path = global_spec_file_path_mock
    spec_file_instance.content = global_spec_mock

    spec_file_instance.write()

    assert decode_logs(caplog.records) == [
        f"DEBUG:mac_maker:{spec_file_instance.Messages.write_start}",
        (
            "DEBUG:mac_maker:" +
            spec_file_instance.Messages.write_end % spec_file_instance.path
        ),
    ]

  class WriteExceptionScenario(NamedTuple):
    set_path: bool
    set_content: bool
    exception: Type[exceptions.SpecFileBaseException]

    def __str__(self) -> str:
      return f"path:{self.set_path},content:{self.set_content}"

  @pytest.mark.parametrize(
      "scenario",
      (
          WriteExceptionScenario(
              set_path=False,
              set_content=True,
              exception=exceptions.SpecFilePathNotDefined,
          ),
          WriteExceptionScenario(
              set_path=True,
              set_content=False,
              exception=exceptions.SpecFileContentNotDefined,
          ),
          WriteExceptionScenario(
              set_path=False,
              set_content=False,
              exception=exceptions.SpecFileContentNotDefined,
          ),
      ),
      ids=str,
  )
  def test_write__vary_unset__raises_exception(
      self,
      global_spec_file_path_mock: str,
      global_spec_mock: Spec,
      spec_file_instance: SpecFile,
      scenario: WriteExceptionScenario,
  ) -> None:
    if scenario.set_path:
      spec_file_instance.path = global_spec_file_path_mock
    if scenario.set_content:
      spec_file_instance.content = global_spec_mock

    with pytest.raises(scenario.exception):
      spec_file_instance.write()
