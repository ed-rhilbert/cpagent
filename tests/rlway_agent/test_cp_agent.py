from rlway_cpagent.cp_agent import CPAgent


def test_cp_agent(osrd_point_switch):
    """Testing no exception raised during regulation

    Parameters
    ----------
    osrd_point_switch : _type_
        _description_
    """
    agent = CPAgent("cp_agent")
    osrd_point_switch.regulate(agent)
