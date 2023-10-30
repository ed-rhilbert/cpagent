from rlway_cpagent.minizinc_agent.minizinc_agent import (
    MinizincAgent,
)


def test_minizinc_agent(osrd_point_switch):
    """Testing no exception raised during regulation

    Parameters
    ----------
    osrd_point_switch : _type_
        _description_
    """
    agent = MinizincAgent("minizinc_agent")
    osrd_point_switch.regulate(agent)
