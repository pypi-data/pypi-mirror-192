"""Constant values for DSL Compiler."""

# The parameter name for pipeline root in PipelineRuntimeSpec.
PIPELINE_ROOT_PARAMETER_NAME = "pipeline-root"

# The parameter name for pipeline run id in PipelineRuntimeSpec.
PIPELINE_RUN_ID_PARAMETER_NAME = "pipeline-run-id"

# The type name for the contexts representing different pipelines.
PIPELINE_CONTEXT_TYPE_NAME = "pipeline"

# The type name for the contexts representing different pipeline runs.
PIPELINE_RUN_CONTEXT_TYPE_NAME = "pipeline_run"

# The type name for the contexts representing different nodes. Note that a
# context of this type only covers node runs within a pipeline domain but not
# across pipelines.
NODE_CONTEXT_TYPE_NAME = "node"

# Class path to the conditional resolver.
CONDITIONAL_RESOLVER_CLASS_PATH = "tfx.dsl.input_resolution.strategies.conditional_strategy.ConditionalStrategy"

# The suffix for a PipelineBegin node's type name and id
PIPELINE_BEGIN_NODE_SUFFIX = "_begin"

# The suffix for a PipelineEnd node's type name and id
PIPELINE_END_NODE_SUFFIX = "_end"
