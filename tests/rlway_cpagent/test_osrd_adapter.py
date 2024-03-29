import pytest

from copy import deepcopy


from rlway_cpagent.osrd_adapter import (
    regulation_problem_from_osrd,
    osrd_stops_from_solution,
    regulation_problem_from_schedule,
    schedule_from_solution,
)
from rlway_cpagent.regulation_solver import (
    CpRegulationProblem,
    CpRegulationSolution,
    OptimisationStatus,
)


def test_regulation_problem_from_osrd(osrd_point_switch):
    """Testing convertion from osrd to cp problem
    """
    cp_problem = regulation_problem_from_osrd(osrd_point_switch)

    oracle_problem = CpRegulationProblem(2, 4)
    oracle_problem.add_step(0, 0, -1, 0, 242, 642, False, 1, 0)
    oracle_problem.add_step(0, 1, 0, 236, 247, 11, True, 1, 5)
    oracle_problem.add_step(0, 2, 1, 242, 450, 208, True, 1, 5)
    oracle_problem.add_step(1, 3, -1, 100, 342, 242, False, 1, 0)
    oracle_problem.add_step(1, 1, 3, 336, 347, 11, True, 1, 5)
    oracle_problem.add_step(1, 0, 4, 342, 550, 208, True, 1, 5)

    assert cp_problem.__dict__ == oracle_problem.__dict__


def test_osrd_stops_from_solution(osrd_point_switch):
    """Testing convertion from solution to osrd stops
    """
    cp_problem = regulation_problem_from_osrd(osrd_point_switch)
    solution = CpRegulationSolution(
        cp_problem,
        OptimisationStatus.OPTIMAL,
        0,
        [0, 236, 242, 100, 336, 342],
        [242, 247, 450, 442, 347, 550])

    stops = osrd_stops_from_solution(osrd_point_switch, solution)

    assert stops == [
        {
            "train": 1,
            "position": 9750.0,
            "duration": 100
        }
    ]


def test_osrd_stops_from_solution_empty(osrd_point_switch):
    """Testing convertion from solution to osrd stops
    with an empty invalid solution
    """
    cp_problem = regulation_problem_from_osrd(osrd_point_switch)
    solution = CpRegulationSolution(
        cp_problem,
        OptimisationStatus.FAILED,
        0,
        [0, 236, 242, 100, 336, 342],
        [242, 247, 450, 442, 347, 600])

    stops = osrd_stops_from_solution(osrd_point_switch, solution)

    assert not stops


def test_osrd_stops_from_solution_invalid_stop(osrd_point_switch):
    """Testing convertion from solution to osrd stops
    with an invalid solution
    """
    cp_problem = regulation_problem_from_osrd(osrd_point_switch)
    solution = CpRegulationSolution(
        cp_problem,
        OptimisationStatus.OPTIMAL,
        None,
        None,
        None)

    with pytest.raises(Exception):
        osrd_stops_from_solution(osrd_point_switch, solution)


def test_regulation_problem_from_schedule(schedule_straight_line_2t):
    cp_problem = regulation_problem_from_schedule(*schedule_straight_line_2t)

    oracle_problem = CpRegulationProblem(2, 2)
    oracle_problem.add_step(0, 0, -1, 0, 10, 10, True)
    oracle_problem.add_step(0, 1, 0, 10, 20, 20, False)
    oracle_problem.add_step(1, 0, -1, 10, 20, 10, False)
    oracle_problem.add_step(1, 1, 2, 20, 30, 10, False)

    assert cp_problem.__dict__ == oracle_problem.__dict__


def test_schedule_from_solution(schedule_straight_line_2t):
    cp_problem = regulation_problem_from_schedule(*schedule_straight_line_2t)
    solution = CpRegulationSolution(
        cp_problem,
        OptimisationStatus.OPTIMAL,
        0,
        [0, 10, 10, 30],
        [10, 30, 30, 40])

    ref_schedule = schedule_straight_line_2t[0]
    regulated_schedule = schedule_from_solution(ref_schedule, solution)

    oracle_regulated = deepcopy(schedule_straight_line_2t[1])
    oracle_regulated.set(1, 0, [10, 30])
    oracle_regulated.set(1, 1, [30, 40])

    assert (regulated_schedule.durations
            == oracle_regulated.durations).all().all()
    assert (regulated_schedule.starts
            == oracle_regulated.starts).all().all()
    assert (regulated_schedule.ends
            == oracle_regulated.ends).all().all()
