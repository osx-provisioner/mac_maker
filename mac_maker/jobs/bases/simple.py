"""SimpleJobBase class."""

import abc


class SimpleJobBase(abc.ABC):
  """Job base class, that doesn't require provisioning."""

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke a simple Job that doesn't require provisioning."""
    raise NotImplementedError  # nocover
