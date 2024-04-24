import pytest

from cpagent.ortools_agent.ortools_agent import (
    OrtoolsAgent,
    OptimisationStatus
)
from cpagent.utils import check_solution_validity, build_solution


@pytest.mark.parametrize("use_case,solver", [
    ("use_case_cp_4_zones_switch", OrtoolsAgent("ortools")),
    ("use_case_delay_conv", OrtoolsAgent("ortools"))
])
def test_solver_feasible(use_case, solver, request):
    """Test the validity of the solution returned by
    the solvers and ortools for the use cases
    use_case_cp_4_zones_switch and use_case_delay_conv
    """
    cp_solver, _ = solver._solve_from_steps(
        request.getfixturevalue(use_case)[0],
        request.getfixturevalue(use_case)[1],
        request.getfixturevalue(use_case)[2]
    )
    assert check_solution_validity(build_solution(solver, cp_solver))


@pytest.mark.parametrize("solver", [
    OrtoolsAgent("ortools")
])
def test_solver_simple(solver, use_case_straight_line_2t):
    """Testing solver on a simple use case
    """
    cp_solver, _ = solver._solve_from_steps(
        use_case_straight_line_2t[0],
        use_case_straight_line_2t[1],
        use_case_straight_line_2t[2]
    )
    cp_solver.Values(solver.arrivals).to_list()
    cost_oracle = 10
    arrivals_oracle = [0, 10, 10, 30]
    departures_oracle = [10, 30, 30, 40]
    assert int(cp_solver.ObjectiveValue()) == cost_oracle
    assert cp_solver.Values(solver.arrivals).to_list() == arrivals_oracle
    assert cp_solver.Values(solver.departures).to_list() == departures_oracle


@pytest.mark.parametrize("solver", [
    OrtoolsAgent("ortools")
])
def test_solver_infeasible(solver, use_case_infeasible):
    """Test solver with infeasible problem
    """
    _, status = solver._solve_from_steps(
        use_case_infeasible[0],
        use_case_infeasible[1],
        use_case_infeasible[2],
    )
    status = solver.status_map[status]
    assert status == OptimisationStatus.FAILED


@pytest.mark.parametrize("solver", [
    OrtoolsAgent("ortools")
])
def test_solver_empty_zone(solver, use_case_empty_zone):
    """Test that solvers can deal with zones with no
    associated train
    """
    cp_solver, _ = solver._solve_from_steps(
        use_case_empty_zone[0],
        use_case_empty_zone[1],
        use_case_empty_zone[2],
    )
    assert check_solution_validity(build_solution(
        solver,
        cp_solver
    ))
