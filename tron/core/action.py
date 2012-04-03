import logging

log = logging.getLogger(__name__)

CLEANUP_ACTION_NAME = 'cleanup'


class Action(object):
    """A configurable data object for an Action."""

    def __init__(self, name, command, node_pool, required_actions=None,
                dependent_actions=None, cleanup=False):
        self.name               = name
        self.command            = command
        self.node_pool          = node_pool
        self.required_actions   = required_actions or []
        self.dependent_actions  = dependent_actions or []
        self.is_cleanup         = cleanup

    @classmethod
    def from_config(cls, config, node_pools, cleanup=False):
        """Factory method for creating a new Action."""
        return cls(
            name=       config.name,
            command=    config.command,
            node_pool=  node_pools[config.node] if config.node else None,
            cleanup=    cleanup
        )

    def __eq__(self, other):
        if (not isinstance(other, Action) or
                self.name       != other.name or
                self.command    != other.command or
                self.node_pool  != other.node_pool or
                self.is_cleanup != other.is_cleanup):
            return False

        return all(
            self_act == other_act for (self_act, other_act)
            in zip(self.required_actions, other.required_actions)
        )

    def __ne__(self, other):
        return not self == other
