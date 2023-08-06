"""Runner base class"""

import abc
from typing import Any, Optional


class BaseRunner(metaclass=abc.ABCMeta):
    """Base class for the studio runner

    This is the base class for every aus runner
    """
    @abc.abstractmethod
    def run(self, workflow, run_options, **kwargs) -> Optional[Any]:
        """Runs Aus workflow on a specific platform

        Args:
            workflow: a workflow.Workflow instance representing a workflow definition
            run_options: an Optional workflow.RunOptions object. See the class
            definition workflow.RunOptions for details. If None, runs the full workflow
            kwargs: extra orchestrator backend-specific keyword arguments.
        Returns:
            Optional platform-specific object
        """
        pass


class IntermediateRepresentationRunner(metaclass=abc.ABCMeta):
    """Base class for the studio runner

    This is the base class for every aus runner
    """
