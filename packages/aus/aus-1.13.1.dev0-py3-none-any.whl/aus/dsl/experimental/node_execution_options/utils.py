"""Utils for user facing SYNC pipeline node execution options.
This is only used for the experimental orchestrator.
"""
import dataclasses

from aus.proto.orchestration import pipeline_pb2


@dataclasses.dataclass
class NodeExecutionOptions:
  """Component Node Execution Options.
  Currently only apply in experimental orchestrator.
  """
  trigger_strategy: pipeline_pb2.NodeExecutionOptions.TriggerStrategy = (
      pipeline_pb2.NodeExecutionOptions.TRIGGER_STRATEGY_UNSPECIFIED)
  success_optional: bool = False
  max_execution_retries: int = 0
  execution_timeout_sec: int = 0

  def __post_init__(self):
    self.max_execution_retries = max(self.max_execution_retries, 0)
