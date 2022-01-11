"""Custom Decorators."""

from functools import wraps
from pathlib import Path
from typing import Callable, Optional, TypeVar, Union

TypeWrappableMethod = TypeVar('TypeWrappableMethod', bound=Callable[..., Path])
TypeSelfArgument = TypeVar('TypeSelfArgument')
TypeWrappedMethod = Callable[..., Union[Path, str]]


def convertible_path(method: TypeWrappableMethod) -> TypeWrappedMethod:
  """Allow a method that returns `pathlib.Path` to optionally return `str`.

  :param method: A method returning :class:`pathlib.Path`.
  :return: The decorated method.
  """

  @wraps(method)
  def decorator(self: TypeSelfArgument,
                string: Optional[bool] = False) -> Union[Path, str]:
    value: Path = method(self)
    if string:
      return str(value.resolve())
    return value

  return decorator
