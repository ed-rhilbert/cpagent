"""
Testing utils.py module
"""

from rlway_cpagent.regulation_solver import (
    CpRegulationSolution,
    OptimisationStatus,
)
from rlway_cpagent.utils import (
    check_solution_validity,
    check_spacing,
    check_chaining,
    check_min_arrival,
    check_min_departure,
    check_min_duration,
    check_fixed_duration,
    check_first_step,
    check_objective_value,
)


def test_check_solution_validity_valid(use_case_cp_4_zones_switch):
    """Test method check_solution_validity with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_solution_validity(solution)


def test_check_solution_validity_invalid(use_case_cp_4_zones_switch):
    """Test method check_solution_validity with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 30, 40, 50],
        [20, 30, 40, 40, 50, 60])

    assert not check_solution_validity(solution)


def test_check_spacing_valid(use_case_cp_4_zones_switch):
    """Test method check_spacing with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_spacing(solution)


def test_check_spacing_invalid(use_case_cp_4_zones_switch):
    """Test method check_spacing with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 10, 20, 30],
        [20, 30, 40, 20, 30, 40])

    assert not check_spacing(solution)


def test_check_chaining_valid(use_case_cp_4_zones_switch):
    """Test method check_chaining with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_chaining(solution)


def test_check_chaining_invalid(use_case_cp_4_zones_switch):
    """Test method check_chaining with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 35, 40],
        [20, 30, 40, 30, 40, 50])

    assert not check_chaining(solution)


def test_check_min_arrival_valid(use_case_cp_4_zones_switch):
    """Test method check_min_arrival with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_min_arrival(solution)


def test_check_min_arrival_invalid(use_case_cp_4_zones_switch):
    """Test method check_min_arrival with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 25, 40],
        [20, 30, 40, 25, 40, 50])

    assert not check_min_arrival(solution)


def test_check_min_departure_valid(use_case_cp_4_zones_switch):
    """Test method check_min_departure with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_min_departure(solution)


def test_check_min_departure_invalid(use_case_cp_4_zones_switch):
    """Test method check_min_departure with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 25, 40],
        [20, 30, 40, 25, 40, 50])

    assert not check_min_departure(solution)


def test_check_min_duration_valid(use_case_cp_4_zones_switch):
    """Test method check_min_duration with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_min_duration(solution)


def test_check_min_duration_invalid(use_case_cp_4_zones_switch):
    """Test method check_min_duration with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 25, 40],
        [20, 30, 40, 25, 40, 50])

    assert not check_min_duration(solution)


def test_check_fixed_duration_valid(use_case_cp_4_zones_switch):
    """Test method check_fixed_duration with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_fixed_duration(solution)


def test_check_fixed_duration_invalid(use_case_cp_4_zones_switch):
    """Test method check_fixed_duration with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 50],
        [20, 30, 40, 30, 50, 60])

    assert not check_fixed_duration(solution)


def test_check_first_step_valid(use_case_cp_4_zones_switch):
    """Test method check_first_step with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert check_first_step(solution)


def test_check_first_step_invalid(use_case_cp_4_zones_switch):
    """Test method check_first_step with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 30, 40, 50],
        [20, 30, 40, 40, 50, 60])

    assert not check_first_step(solution)


def test_check_objective_value(use_case_cp_4_zones_switch):
    """Test method check_objective_value with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        40,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])
    assert check_objective_value(solution)


def test_check_objective_value_invalid(use_case_cp_4_zones_switch):
    """Test method check_objective_value with invalid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch,
        OptimisationStatus.OPTIMAL,
        10,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert not check_objective_value(solution)
