"""TFX Conditionals."""
from typing import Sequence

import attr
from aus.dsl.widgets.base import base_node
from aus.dsl.context_managers import dsl_context
from aus.dsl.context_managers import dsl_context_manager
from aus.dsl.context_managers import dsl_context_registry
from aus.dsl.placeholder import placeholder


@attr.s(auto_attribs=True, kw_only=True, hash=False, eq=False)
class CondContext(dsl_context.DslContext):
    """DslContext for Cond."""
    predicate: placeholder.Predicate

    def validate(self, containing_nodes: Sequence[base_node.BaseNode]):
        if any(p.predicate == self.predicate
               for p in self.ancestors
               if isinstance(p, CondContext)):
            raise ValueError(
                f'Nested conditionals with duplicate predicates: {self.predicate}.'
                'Consider merging the nested conditionals.')


def get_predicates(
        node: base_node.BaseNode,
        reg: dsl_context_registry.DslContextRegistry,
) -> Sequence[placeholder.Predicate]:
    """Gets all predicates that conditional contexts for the node carry."""
    return tuple(c.predicate
                 for c in reg.get_contexts(node)
                 if isinstance(c, CondContext))


class Cond(dsl_context_manager.DslContextManager[None]):
    """Cond context manager that disable containing nodes if predicate is False.
  Cond blocks can be nested to express the nested conditions.
  Usage:
    evaluator = Evaluator(
        examples=example_gen.outputs['examples'],
        model=trainer.outputs['model'],
        eval_config=EvalConfig(...))
    with Cond(evaluator.outputs['blessing'].future()
              .custom_property('blessed') == 1):
      pusher = Pusher(
          model=trainer.outputs['model'],
          push_destination=PushDestination(...))
  """

    def __init__(self, predicate: placeholder.Predicate):
        super().__init__()
        self._predicate = predicate

    def create_context(self) -> CondContext:
        return CondContext(predicate=self._predicate)

    def enter(  # pytype: disable=signature-mismatch  # overriding-parameter-type-checks
            self, context: CondContext) -> None:  # pylint: disable=unused-argument
        return None
