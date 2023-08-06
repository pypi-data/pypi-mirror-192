"""Interface for filesystem plugins."""

from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

PathType = Union[bytes, str]


class NotFoundError(IOError):
  pass


class Filesystem:
  """Abstract Filesystem class."""

  SUPPORTED_SCHEMES = []

  @staticmethod
  def open(name: PathType, mode: str = 'r') -> Any:
    raise NotImplementedError()

  @staticmethod
  def copy(src: PathType, dst: PathType, overwrite: bool = False) -> None:
    raise NotImplementedError()

  @staticmethod
  def exists(path: PathType) -> bool:
    raise NotImplementedError()

  @staticmethod
  def glob(pattern: PathType) -> List[PathType]:
    raise NotImplementedError()

  @staticmethod
  def isdir(path: PathType) -> bool:
    raise NotImplementedError()

  @staticmethod
  def listdir(path: PathType) -> List[PathType]:
    raise NotImplementedError()

  @staticmethod
  def makedirs(path: PathType) -> None:
    raise NotImplementedError()

  @staticmethod
  def mkdir(path: PathType) -> None:
    raise NotImplementedError()

  @staticmethod
  def remove(path: PathType) -> None:
    raise NotImplementedError()

  @staticmethod
  def rename(src: PathType, dst: PathType, overwrite: bool = False) -> None:
    raise NotImplementedError()

  @staticmethod
  def rmtree(path: PathType) -> None:
    raise NotImplementedError()

  @staticmethod
  def stat(path: PathType) -> Any:
    raise NotImplementedError()

  @staticmethod
  def walk(
      top: PathType,
      topdown: bool = True,
      onerror: Optional[Callable[..., None]] = None
  ) -> Iterable[Tuple[PathType, List[PathType], List[PathType]]]:
    raise NotImplementedError()

  @staticmethod
  def get_inline_filename(data: str, compressed: bool = False) -> str:
    raise NotImplementedError()
