from rlway_cpagent.minizinc_agent.minizinc_agent import (
    MinizincAgent,
)


def test_minizinc_agent(osrd_point_switch):
    """Testing no exception raised during regulation
    """
    agent = MinizincAgent("minizinc_agent")
    osrd_point_switch.regulate(agent)
