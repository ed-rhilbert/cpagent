import pytest

from rlway_cpagent.ortools_agent.ortools_solver import (
    OrtoolsRegulationSolver,
)
from rlway_cpagent.regulation_solver import OptimisationStatus
from rlway_cpagent.utils import check_solution_validity


@pytest.mark.parametrize("use_case,solver", [
    ("use_case_cp_4_zones_switch", OrtoolsRegulationSolver("ortools", 30)),
    ("use_case_delay_conv", OrtoolsRegulationSolver("ortools", 30))
])
def test_solver_feasible(use_case, solver, request):
    """Test the validity of the solution returned by
    the solvers and ortools for the use cases
    use_case_cp_4_zones_switch and use_case_delay_conv
    """
    solution = solver.solve(request.getfixturevalue(use_case))
    assert check_solution_validity(solution)


@pytest.mark.parametrize("solver", [
    OrtoolsRegulationSolver("ortools", 30)
])
def test_solver_simple(solver, use_case_straight_line_2t):
    """Testing solver on a simple use case
    """
    solution = solver.solve(use_case_straight_line_2t)
    cost_oracle = 10
    arrivals_oracle = [0, 10, 10, 30]
    departures_oracle = [10, 30, 30, 40]
    assert solution.cost == cost_oracle
    assert solution.arrivals == arrivals_oracle
    assert solution.departures == departures_oracle


@pytest.mark.parametrize("solver", [
    OrtoolsRegulationSolver("ortools", 30)
])
def test_solver_infeasible(solver, use_case_infeasible):
    """Test solver with infeasible problem
    """
    solution = solver.solve(use_case_infeasible)
    assert solution.status == OptimisationStatus.FAILED


@pytest.mark.parametrize("solver", [
    OrtoolsRegulationSolver("ortools", 30)
])
def test_solver_empty_zone(solver, use_case_empty_zone):
    """Test that solvers can deal with zones with no
    associated train
    """
    solution = solver.solve(use_case_empty_zone)
    assert check_solution_validity(solution)
