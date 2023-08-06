"""A set of TFX System Artifacts.
It matches the MLMD system artifacts types from:
third_party/ml_metadata/metadata_store/mlmd_types.py
"""
import abc
from ml_metadata.metadata_store import mlmd_types


class SystemArtifact(abc.ABC):
    """TFX system artifact base class.
  A user may create a subclass of SystemArtifact and override the
  MLMD_SYSTEM_BASE_TYPE property with the MLMD system type enum.
  The subclasses, e.g, Dataset, Model, Statistics, e.t.c, match the MLMD types
  from third_party/ml_metadata/metadata_store/mlmd_types.py.
  """

    # MLMD system base type enum. Override it when creating subclasses.
    MLMD_SYSTEM_BASE_TYPE = None


class Dataset(SystemArtifact):
    """Dataset is a TFX pre-defined system artifact."""
    MLMD_SYSTEM_BASE_TYPE = mlmd_types.Dataset().system_type


class Model(SystemArtifact):
    """Model is a TFX pre-defined system artifact."""
    MLMD_SYSTEM_BASE_TYPE = mlmd_types.Model().system_type


class Statistics(SystemArtifact):
    """Statistics is a TFX pre-defined system artifact."""
    MLMD_SYSTEM_BASE_TYPE = mlmd_types.Statistics().system_type
