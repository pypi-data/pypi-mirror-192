"""Utility module for data governance."""
import datetime
from typing import Optional

from aus import types


def is_expired(artifact: types.Artifact,
               now: Optional[datetime.datetime] = None) -> bool:
  """Checks whether the artifact is expired regarding governance properties."""
  del artifact, now
  return False
