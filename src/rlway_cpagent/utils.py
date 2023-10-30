from typing import Any, Dict, List
from itertools import permutations

from rlway_cpagent.regulation_solver import CpRegulationSolution


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
    for zone_idx in range(cp_solution.problem.nb_zones):
        intervals = [
            (cp_solution.arrivals[idx], cp_solution.departures[idx])
            for idx, step in enumerate(cp_solution.problem.steps)
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
        for step_idx, step in enumerate(cp_solution.problem.steps)
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
        for step_idx, step in enumerate(cp_solution.problem.steps)
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
        for step_idx, step in enumerate(cp_solution.problem.steps)
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
        for step_idx, step in enumerate(cp_solution.problem.steps)
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
        for step_idx, step in enumerate(cp_solution.problem.steps)
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
        for step_idx, step in enumerate(cp_solution.problem.steps)
        if step["prev"] == -1
    )
