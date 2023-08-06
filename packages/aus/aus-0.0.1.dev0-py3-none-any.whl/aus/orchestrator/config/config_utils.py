"""Utilities for handling common config operations."""

from typing import Optional, Tuple, Type

from aus.dsl.widgets.base import base_component
from aus.orchestrator.config import base_component_config
from aus.orchestrator.config import pipeline_config
from aus.orchestrator.launcher import base_component_launcher


def find_component_launch_info(
    p_config: pipeline_config.PipelineConfig,
    component: base_component.BaseComponent,
) -> Tuple[Type[base_component_launcher.BaseComponentLauncher],
           Optional[base_component_config.BaseComponentConfig]]:
  """Find a launcher and component config to launch the component.
  The default lookup logic goes through the `supported_launcher_classes`
  in sequence for each config from the `default_component_configs`. User can
  override a single component setting by `component_config_overrides`. The
  method returns the first component config and launcher which together can
  launch the executor_spec of the component.
  Subclass may customize the logic by overriding the method.
  Args:
    p_config: the pipeline config.
    component: the component to launch.
  Returns:
    The found tuple of component launcher class and the compatible component
    config.
  Raises:
    RuntimeError: if no supported launcher is found.
  """
  if component.id in p_config.component_config_overrides:
    component_configs = [p_config.component_config_overrides[component.id]]
  else:
    # Add None to the end of the list to find launcher with no component
    # config
    component_configs = p_config.default_component_configs + [None]

  for component_config in component_configs:
    for component_launcher_class in p_config.supported_launcher_classes:
      if component_launcher_class.can_launch(component.executor_spec,
                                             component_config):
        return (component_launcher_class, component_config)
  raise RuntimeError('No launcher info can be found for component "%s".' %
                     component.component_id)
