from .planner import policy


def agent(observation, configuration=None):
    return policy(observation, configuration)
