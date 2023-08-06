"""Experimental Resolver for getting the latest artifact."""

from typing import Dict, List, Optional

from aus import types
from aus.dsl.widgets.common import resolver

import ml_metadata as mlmd


class LatestArtifactStrategy(resolver.ResolverStrategy):
  """Strategy that resolves the latest n(=1) artifacts per each channel.
  Note that this ResolverStrategy is experimental and is subject to change in
  terms of both interface and implementation.
  Don't construct LatestArtifactStrategy directly, example usage:
  ```
    model_resolver = Resolver(
        strategy_class=LatestArtifactStrategy,
        model=Channel(type=Model),
    ).with_id('latest_model_resolver')
    model_resolver.outputs['model']
  ```
  """

  def __init__(self, desired_num_of_artifacts: Optional[int] = 1):
    self._desired_num_of_artifact = desired_num_of_artifacts

  def _resolve(self, input_dict: Dict[str, List[types.Artifact]]):
    result = {}
    for k, artifact_list in input_dict.items():
      sorted_artifact_list = sorted(
          artifact_list, key=lambda a: a.id, reverse=True)
      result[k] = sorted_artifact_list[:min(
          len(sorted_artifact_list), self._desired_num_of_artifact)]
    return result

  def resolve_artifacts(
      self, store: mlmd.MetadataStore,
      input_dict: Dict[str, List[types.Artifact]]
  ) -> Optional[Dict[str, List[types.Artifact]]]:
    """Resolves artifacts from channels by querying MLMD.
    Args:
      store: An MLMD MetadataStore object.
      input_dict: The input_dict to resolve from.
    Returns:
      If `min_count` for every input is met, returns a
      Dict[str, List[Artifact]]. Otherwise, return None.
    """
    resolved_dict = self._resolve(input_dict)
    all_min_count_met = all(
        len(artifact_list) >= self._desired_num_of_artifact
        for artifact_list in resolved_dict.values())
    return resolved_dict if all_min_count_met else None
