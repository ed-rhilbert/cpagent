"""
Testing utils.py module
"""
from itertools import permutations

from cpagent.solution import (
    CpRegulationSolution,
)


def test_check_solution_validity_valid(use_case_cp_4_zones_switch):
    """Test method check_solution_validity with valid solution

    Parameters
    ----------
    use_case_cp_4_zones_switch : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
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
        use_case_cp_4_zones_switch[0],
        use_case_cp_4_zones_switch[1],
        use_case_cp_4_zones_switch[2],
        10,
        [0, 20, 30, 20, 30, 40],
        [20, 30, 40, 30, 40, 50])

    assert not check_objective_value(solution)


def check_solution_validity(cp_solution: CpRegulationSolution) -> bool:
    """Checks that a given solution respect all the constraints

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        solution returned by the solver

    Returns
    -------
    bool
        true if all constraints are respected
    """
    return (
        check_spacing(cp_solution)
        and check_chaining(cp_solution)
        and check_min_arrival(cp_solution)
        and check_min_departure(cp_solution)
        and check_min_duration(cp_solution)
        and check_fixed_duration(cp_solution)
        and check_first_step(cp_solution)
        and check_objective_value(cp_solution)
    )


def check_spacing(cp_solution: CpRegulationSolution) -> bool:
    """Check if a given solution to a cp problem respects the spacing
    constraint

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        cp solution returned by solver

    Returns
    -------
    bool
        true if the solution respects the constraint
    """
    is_overlapping = []
    for zone_idx in range(cp_solution.nb_zones):
        intervals = [
            (cp_solution.arrivals[idx], cp_solution.departures[idx])
            for idx, step in enumerate(cp_solution.steps)
            if step["zone"] == zone_idx
        ]
        is_overlapping.append(any([i1[1] > i2[0] and i1[0] < i2[1]
                              for i1, i2 in permutations(intervals, 2)]))
    return not any(is_overlapping)


def check_chaining(cp_solution: CpRegulationSolution) -> bool:
    """Checks if the solution respects the chaing of the steps
    (the departure of a step must match the arrival of the next step)

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        solution returned by a solver

    Returns
    -------
    bool
        True if the solution respect the constraint
    """
    return not any([
        cp_solution.departures[step["prev"]] != cp_solution.arrivals[step_idx]
        for step_idx, step in enumerate(cp_solution.steps)
        if step["prev"] != -1
    ])


def check_min_arrival(cp_solution: CpRegulationSolution) -> bool:
    """Check if a step arrives after the reference

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        Solution returned by a solver

    Returns
    -------
    bool
        True if the solution respect the constraint
    """
    return not any(
        cp_solution.arrivals[step_idx] < step["min_arrival"]
        for step_idx, step in enumerate(cp_solution.steps)
    )


def check_min_departure(cp_solution: CpRegulationSolution) -> bool:
    """Check if a step leaves after the reference

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        Solution returned by a solver

    Returns
    -------
    bool
        True if the solution respect the constraint
    """
    return not any(
        cp_solution.departures[step_idx] < step["min_departure"]
        for step_idx, step in enumerate(cp_solution.steps)
    )


def check_min_duration(cp_solution: CpRegulationSolution) -> bool:
    """Check if each step last longer than the minimum duration

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        the solution returned by a solver

    Returns
    -------
    bool
        True if the solution respects the constraint
    """
    return not any(
        cp_solution.departures[step_idx] - cp_solution.arrivals[step_idx]
        < step["min_duration"]
        for step_idx, step in enumerate(cp_solution.steps)
    )


def check_fixed_duration(cp_solution: CpRegulationSolution) -> bool:
    """Checks that if a step is fixed then its duration is unchanged

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        solution returned by a solver

    Returns
    -------
    bool
        True if the constraint is respected
    """
    return not any(
        cp_solution.departures[step_idx] - cp_solution.arrivals[step_idx]
        != step["min_duration"]
        for step_idx, step in enumerate(cp_solution.steps)
        if step["is_fixed"] is True
    )


def check_first_step(cp_solution: CpRegulationSolution) -> bool:
    """Checks that each first step arrival is unchanged

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        solution returned by the solver

    Returns
    -------
    bool
        True if the constraint is respected
    """
    return not any(
        cp_solution.arrivals[step_idx] != step["min_arrival"]
        for step_idx, step in enumerate(cp_solution.steps)
        if step["prev"] == -1
    )


def check_objective_value(cp_solution: CpRegulationSolution) -> bool:
    """Check that the objective value match the sum of departure
    delays

    Parameters
    ----------
    cp_solution : CpRegulationSolution
        solution returned by the solver

    Returns
    -------
    bool
        True if the objective value match the sum of the departure delays
    """
    return cp_solution.cost == sum(
        [
            (cp_solution.arrivals[i] - step["min_arrival"])
            * step["ponderation"]
            for i, step in enumerate(cp_solution.steps)
        ]
    )
