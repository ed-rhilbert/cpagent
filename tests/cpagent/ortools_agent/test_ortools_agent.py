from cpagent.cp_agent import (
    CpAgent,
)


def test_ortools_agent(osrd_point_switch):
    """Testing no exception raised during regulation
    """
    agent = CpAgent("ortools_agent")
    osrd_point_switch.regulate(agent)
