from rlway_cpagent.ortools_agent.ortools_agent import (
    OrtoolsAgent,
)


def test_ortools_agent(osrd_point_switch):
    """Testing no exception raised during regulation

    Parameters
    ----------
    osrd_point_switch : _type_
        _description_
    """
    agent = OrtoolsAgent("ortools_agent")
    osrd_point_switch.regulate(agent)
