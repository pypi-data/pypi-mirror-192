"""Definition of TFX runner base class."""

import abc
from typing import Any, Optional

from aus.orchestrator.config import pipeline_config


class TfxRunner(abc.ABC):
  """Base runner class for TFX.
  This is the base class for every TFX runner.
  """

  def __init__(self, config: Optional[pipeline_config.PipelineConfig] = None):
    """Initializes a TfxRunner instance.
    Args:
      config: Optional pipeline config for customizing the launching
        of each component.
    """
    self._config = config or pipeline_config.PipelineConfig()

  @abc.abstractmethod
  def run(self, pipeline) -> Optional[Any]:
    """Runs logical TFX pipeline on specific platform.
    Args:
      pipeline: logical TFX pipeline definition.
    Returns:
      Platform-specific object.
    """
    pass

  @property
  def config(self) -> pipeline_config.PipelineConfig:
    return self._config
