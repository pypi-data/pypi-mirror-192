"""A class to define how to operator an python based driver."""

from typing import cast

from aus.orchestrator import metadata
from aus.orchestrator.portable import base_driver_operator
from aus.orchestrator.portable import data_types
from aus.proto.orchestration import driver_output_pb2
from aus.proto.orchestration import executable_spec_pb2
from aus.proto.orchestration import pipeline_pb2
from aus.utils import import_utils

from google.protobuf import message


class PythonDriverOperator(base_driver_operator.BaseDriverOperator):
  """PythonDriverOperator handles python class based driver's init and execution."""

  SUPPORTED_EXECUTABLE_SPEC_TYPE = [
      executable_spec_pb2.PythonClassExecutableSpec
  ]

  def __init__(self, driver_spec: message.Message,
               mlmd_connection: metadata.Metadata):
    """Constructor.
    Args:
      driver_spec: The specification of how to initialize the driver.
      mlmd_connection: ML metadata connection.
    Raises:
      RuntimeError: if the driver_spec is not supported.
    """
    super().__init__(driver_spec, mlmd_connection)

    python_class_driver_spec = cast(
        pipeline_pb2.ExecutorSpec.PythonClassExecutorSpec, driver_spec)
    self._driver = import_utils.import_class_by_path(
        python_class_driver_spec.class_path)(
            self._mlmd_connection)

  def run_driver(
      self, execution_info: data_types.ExecutionInfo
  ) -> driver_output_pb2.DriverOutput:
    return self._driver.run(execution_info)
