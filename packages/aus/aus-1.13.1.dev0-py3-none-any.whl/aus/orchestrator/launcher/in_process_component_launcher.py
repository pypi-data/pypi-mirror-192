"""In process component launcher which launches python executors in process."""

import copy
import os
from typing import Any, Dict, List, cast

from aus import types
from aus.dsl.widgets.base import base_beam_executor
from aus.dsl.widgets.base import base_executor
from aus.dsl.widgets.base import executor_spec
from aus.orchestrator.config import base_component_config
from aus.orchestrator.launcher import base_component_launcher


class InProcessComponentLauncher(base_component_launcher.BaseComponentLauncher):
  """Responsible for launching a python executor.
  The executor will be launched in the same process of the rest of the
  component, i.e. its driver and publisher.
  """

  @classmethod
  def can_launch(
      cls, component_executor_spec: executor_spec.ExecutorSpec,
      component_config: base_component_config.BaseComponentConfig) -> bool:
    """Checks if the launcher can launch the executor spec."""
    if component_config:
      return False

    return isinstance(component_executor_spec, executor_spec.ExecutorClassSpec)

  def _run_executor(self, execution_id: int,
                    input_dict: Dict[str, List[types.Artifact]],
                    output_dict: Dict[str, List[types.Artifact]],
                    exec_properties: Dict[str, Any]) -> None:
    """Execute underlying component implementation."""
    executor_class_spec = cast(executor_spec.ExecutorClassSpec,
                               self._component_executor_spec)

    if issubclass(executor_class_spec.executor_class,
                  base_beam_executor.BaseBeamExecutor):
      executor_context = base_beam_executor.BaseBeamExecutor.Context(
          beam_pipeline_args=self._beam_pipeline_args,
          tmp_dir=os.path.join(self._pipeline_info.pipeline_root, '.temp', ''),
          unique_id=str(execution_id))
    else:
      executor_context = base_executor.BaseExecutor.Context(
          extra_flags=self._beam_pipeline_args,
          tmp_dir=os.path.join(self._pipeline_info.pipeline_root, '.temp', ''),
          unique_id=str(execution_id))

    # Type hint of component will cause not-instantiable error as
    # component.executor is Type[BaseExecutor] which has an abstract function.
    executor = executor_class_spec.executor_class(
        executor_context)  # type: ignore

    # Make a deep copy for input_dict and exec_properties, because they should
    # be immutable in this context.
    # output_dict can still be changed, specifically properties.
    executor.Do(
        copy.deepcopy(input_dict), output_dict, copy.deepcopy(exec_properties))
