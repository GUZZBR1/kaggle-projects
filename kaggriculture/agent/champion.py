from .planner import policy


def agent(observation, configuration=None):
    """Bootstrap policy; release champions are immutable artifacts in versions/."""
    return policy(observation, configuration)
