"""Experimental Resolver for evaluating the condition."""

from typing import Dict, List, Optional

from aus import types
from aus.dsl.compiler import placeholder_utils
from aus.dsl.widgets.common import resolver
from aus.orchestrator import metadata
from aus.orchestrator.portable import data_types as portable_data_types
from aus.orchestrator.portable.input_resolution import exceptions
from aus.proto.orchestration import placeholder_pb2


class ConditionalStrategy(resolver.ResolverStrategy):
    """Strategy that resolves artifacts if predicates are met.
  This resolver strategy is used by TFX internally to support conditional.
  Not intended to be directly used by users.
  """

    def __init__(self, predicates: List[placeholder_pb2.PlaceholderExpression]):
        self._predicates = predicates

    def resolve_artifacts(
            self, metadata_handler: metadata.Metadata,
            input_dict: Dict[str, List[types.Artifact]]
    ) -> Optional[Dict[str, List[types.Artifact]]]:
        for placeholder_pb in self._predicates:
            context = placeholder_utils.ResolutionContext(
                exec_info=portable_data_types.ExecutionInfo(input_dict=input_dict))
            predicate_result = placeholder_utils.resolve_placeholder_expression(
                placeholder_pb, context)
            if not isinstance(predicate_result, bool):
                raise ValueError("Predicate evaluates to a non-boolean result.")

            if not predicate_result:
                raise exceptions.SkipSignal("Predicate evaluates to False.")
        return input_dict
