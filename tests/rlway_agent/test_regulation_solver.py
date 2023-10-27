import pytest

from rlway_cpagent.regulation_solver import (
    CpRegulationProblem,
    CpRegulationSolution,
    CpRegulationSolver,
    MinizincRegulationSolver,
    OptimisationStatus,
)
from rlway_cpagent.utils import check_solution_validity


def test_get_delays(use_case_straight_line_2t):
    """Testing the function get_delays of the class CpRegulationSolution

    Parameters
    ----------
    use_case_straight_line_2t : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_straight_line_2t,
        OptimisationStatus.OPTIMAL,
        [0, 10, 10, 30],
        [10, 30, 30, 40])

    delays_oracle = [
        {
            "train": 2,
            "zone": 1,
            "duration": 10
        }
    ]

    assert solution.get_delays() == delays_oracle


def test_get_delays_empty(use_case_straight_line_2t):
    """Testing the function get_delays of the class CpRegulationSolution
    with an empty solution

    Parameters
    ----------
    use_case_straight_line_2t : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_straight_line_2t,
        OptimisationStatus.FAILED,
        None,
        None)

    delays_oracle = []

    assert solution.get_delays() == delays_oracle


@pytest.mark.parametrize("config", [
    "use_case_cp_4_zones_switch", "use_case_delay_conv"])
def test_minizinc_solver_feasible(config, request):
    """Test the validity of a solution returned by
    the solver minizinc for the use case use_case_cp_4_zones_switch

    Parameters
    ----------
    cp_problem_point_switch : _type_
        _description_
    """
    solver = MinizincRegulationSolver("gecode", 30)
    solution = solver.solve(request.getfixturevalue(config))
    assert check_solution_validity(solution)


def test_minizinc_solver_simple(use_case_straight_line_2t):
    """Testing minizinc solver on a simple use case

    Parameters
    ----------
    use_case_straight_line_2t : _type_
        _description_
    """
    solver = MinizincRegulationSolver("gecode", 30)
    solution = solver.solve(use_case_straight_line_2t)
    arrivals_oracle = [0, 10, 10, 30]
    departures_oracle = [10, 30, 30, 40]
    assert solution.arrivals == arrivals_oracle
    assert solution.departures == departures_oracle


def test_minizinc_solver_infeasible(use_case_infeasible):
    """Test minizinc solver with infeasible problem

    Parameters
    ----------
    cp_problem_point_switch : _type_
        _description_
    """
    solver = MinizincRegulationSolver("gecode", 30)
    solution = solver.solve(use_case_infeasible)
    assert solution.status == OptimisationStatus.FAILED
