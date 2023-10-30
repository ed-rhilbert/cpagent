import pytest

from rlway_cpagent.ortools_agent.ortools_solver import (
    OrtoolsRegulationSolver,
)
from rlway_cpagent.minizinc_agent.minizinc_solver import (
    MinizincRegulationSolver,
)
from rlway_cpagent.regulation_solver import OptimisationStatus
from rlway_cpagent.utils import check_solution_validity


@pytest.mark.parametrize("use_case,solver", [
    ("use_case_cp_4_zones_switch", OrtoolsRegulationSolver()),
    ("use_case_delay_conv", MinizincRegulationSolver("gecode", 30))])
def test_solver_feasible(use_case, solver, request):
    """Test the validity of a solution returned by
    the solver minizinc for the use case use_case_cp_4_zones_switch

    Parameters
    ----------
    cp_problem_point_switch : _type_
        _description_
    """
    solution = solver.solve(request.getfixturevalue(use_case))
    assert check_solution_validity(solution)


@pytest.mark.parametrize("solver", [
    OrtoolsRegulationSolver(),
    MinizincRegulationSolver("gecode", 30)])
def test_solver_simple(solver, use_case_straight_line_2t):
    """Testing minizinc solver on a simple use case

    Parameters
    ----------
    use_case_straight_line_2t : _type_
        _description_
    """
    solution = solver.solve(use_case_straight_line_2t)
    arrivals_oracle = [0, 10, 10, 30]
    departures_oracle = [10, 30, 30, 40]
    print(solution.arrivals)
    print(solution.departures)
    assert solution.arrivals == arrivals_oracle
    assert solution.departures == departures_oracle


@pytest.mark.parametrize("solver", [
    OrtoolsRegulationSolver(),
    MinizincRegulationSolver("gecode", 30)])
def test_solver_infeasible(solver, use_case_infeasible):
    """Test minizinc solver with infeasible problem

    Parameters
    ----------
    cp_problem_point_switch : _type_
        _description_
    """
    solution = solver.solve(use_case_infeasible)
    assert solution.status == OptimisationStatus.FAILED
