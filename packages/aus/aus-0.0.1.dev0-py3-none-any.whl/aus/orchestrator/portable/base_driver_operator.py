"""Base class to define how to operator an executor."""

import abc

from aus.orchestrator import metadata
from aus.orchestrator.portable import data_types
from aus.proto.orchestration import driver_output_pb2
from aus.utils import abc_utils

from google.protobuf import message


class BaseDriverOperator(abc.ABC):
  """The base class of all executor operators."""

  SUPPORTED_EXECUTABLE_SPEC_TYPE = abc_utils.abstract_property()

  def __init__(self, driver_spec: message.Message,
               mlmd_connection: metadata.Metadata):
    """Constructor.
    Args:
      driver_spec: The specification of how to initialize the driver.
      mlmd_connection: ML metadata connection.
    Raises:
      RuntimeError: if the driver_spec is not supported.
    """
    if not isinstance(driver_spec,
                      tuple(t for t in self.SUPPORTED_EXECUTABLE_SPEC_TYPE)):
      raise RuntimeError('Driver spec not supported: %s' % driver_spec)
    self._driver_spec = driver_spec
    self._mlmd_connection = mlmd_connection

  @abc.abstractmethod
  def run_driver(
      self, execution_info: data_types.ExecutionInfo
  ) -> driver_output_pb2.DriverOutput:
    """Invokes the driver with inputs provided by the Launcher.
    Args:
      execution_info: data_types.ExecutionInfo containing information needed for
        driver execution.
    Returns:
      An DriverOutput instance.
    """
    pass
