from cpagent.ortools_agent.ortools_agent import (
    OrtoolsAgent,
)


def test_ortools_agent(osrd_point_switch):
    """Testing no exception raised during regulation
    """
    agent = OrtoolsAgent("ortools_agent")
    osrd_point_switch.regulate(agent)
