"""The base class of all system node handlers."""

import abc

from aus.orchestrator import metadata
from aus.proto.orchestration import pipeline_pb2

from ml_metadata.proto import metadata_store_pb2


class SystemNodeHandler(abc.ABC):
  """SystemNodeHandler is the base class of all system nodes' handler."""

  @abc.abstractmethod
  def run(
      self,
      mlmd_connection: metadata.Metadata,
      pipeline_node: pipeline_pb2.PipelineNode,
      pipeline_info: pipeline_pb2.PipelineInfo,
      pipeline_runtime_spec: pipeline_pb2.PipelineRuntimeSpec
  ) -> metadata_store_pb2.Execution:
    """Runs the system node and return the Execution.
    Args:
      mlmd_connection: ML metadata connection.
      pipeline_node: The specification of the node that this launcher lauches.
      pipeline_info: The information of the pipeline that this node runs in.
      pipeline_runtime_spec: The runtime information of the pipeline that this
        node runs in.
    Returns:
      The execution of the run.
    """
    pass
