from cpagent.cp_agent import (
    CpAgent,
)


def test_cp_agent(osrd_point_switch):
    """Testing no exception raised during regulation
    """
    agent = CpAgent("ortools_agent")
    agent.set_schedules_from_osrd(osrd_point_switch, "all_steps")
    agent.regulated_schedule
