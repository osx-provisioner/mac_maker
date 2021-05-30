"""Custom Decorators."""

from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, Union

TypeF = TypeVar('TypeF', bound=Callable[..., Any])


def convertable_path(method: TypeF):
  """Allows a method that returns `pathlib.Path` to optionally return `str`."""

  @wraps(method)
  def decorator(self=None, string: bool = False) -> Union[Path, str]:

    value = method(self)
    if string:
      return str(value.resolve())
    return value

  return decorator
