"""
Provides adapting function transforming a regulation problem
from an osrd format to a constraint programming format
"""

from typing import Any, Dict, List

from rlway.pyosrd.osrd import OSRD
from rlway.schedules import Schedule, schedule_from_osrd

from rlway_cpagent.regulation_solver import (
    CpRegulationProblem,
    CpRegulationSolution,
    OptimisationStatus,
)


def regulation_problem_from_osrd(osrd: OSRD) -> CpRegulationProblem:
    """Transform a regulation problem from osrd format to constraint
    programming format

    Parameters
    ----------
    osrd : OSRD
        osrd simulation

    Returns
    -------
    CpRegulationProblem
        Constraint programming problem
    """
    ref_schedule = schedule_from_osrd(osrd)
    delayed_schedule = schedule_from_osrd(osrd.delayed())

    zones = ref_schedule.blocks
    trains = ref_schedule.trains

    starts = ref_schedule.starts
    ends = ref_schedule.ends

    delayed_starts = delayed_schedule.starts
    delayed_ends = delayed_schedule.ends

    problem = CpRegulationProblem(len(trains), len(zones))

    for train_idx, _ in enumerate(trains):
        prev_step = -1
        for zone in ref_schedule.trajectory(train_idx):
            problem.add_step(
                train=train_idx,
                zone=zones.index(zone),
                prev_idx=prev_step,
                min_arrival=int(starts.loc[zone][train_idx]),
                min_departure=int(ends.loc[zone][train_idx]),
                min_duration=int(delayed_ends.loc[zone][train_idx])
                - int(delayed_starts.loc[zone][train_idx]),
                is_fixed=True if osrd.stop_positions[train_idx][zone]['offset']
                is None else False
            )
            prev_step = len(problem.steps) - 1

    return problem


def osrd_stops_from_solution(
        osrd: OSRD, solution: CpRegulationSolution) -> List[Dict[str, Any]]:
    """Transform a constraint programming solution to a list of stops

    Parameters
    ----------
    osrd : OSRD
        osrd simulation
    solution : CpRegulationSolution
        solution returned by a constraint programming solver

    Returns
    -------
    List[Dict[str, Any]]
        list of stops
    """
    stops = []
    if solution.status == OptimisationStatus.FAILED:
        return stops
    ref_schedule = schedule_from_osrd(osrd)
    zones = ref_schedule.blocks
    for delay in solution.get_delays():
        pos = osrd.stop_positions[delay["train"]][zones[delay["zone"]]]
        assert pos['offset'] is not None
        stops.append({
            "train": delay["train"],
            "position": pos['offset'],
            "duration": delay["duration"]
        })
    return stops


def regulation_problem_from_schedule(
        ref_schedule: Schedule, delayed_schedule) -> CpRegulationProblem:
    """Convert a schedule into a CpRegulationProblem
    TODO for now, all steps are unfixed

    Parameters
    ----------
    schedule : Schedule
        Input schedule

    Returns
    -------
    CpRegulationProblem
        problem in CpRegulationProblem format
    """
    zones = ref_schedule.blocks
    trains = ref_schedule.trains

    starts = ref_schedule.starts
    ends = ref_schedule.ends

    delayed_starts = delayed_schedule.starts
    delayed_ends = delayed_schedule.ends

    problem = CpRegulationProblem(len(trains), len(zones))

    for train_idx, _ in enumerate(trains):
        prev_step = -1
        for zone in ref_schedule.trajectory(train_idx):
            problem.add_step(
                train=train_idx,
                zone=zones.index(zone),
                prev_idx=prev_step,
                min_arrival=int(starts.loc[zone][train_idx]),
                min_departure=int(ends.loc[zone][train_idx]),
                min_duration=int(delayed_ends.loc[zone][train_idx])
                - int(delayed_starts.loc[zone][train_idx]),
                is_fixed=False
            )
            prev_step = len(problem.steps) - 1

    return problem


def schedule_from_solution(solution: CpRegulationSolution) -> Schedule:
    """Generate a regulated Schedule from a CpRegulationSolution

    Parameters
    ----------
    solution : CpRegulationSolution
        The solution returned by the cp solver

    Returns
    -------
    Schedule
        The regulated Shchedule
    """
    regulated_schedule = Schedule(
        solution.problem.nb_zones,
        solution.problem.nb_trains)

    if solution.status == OptimisationStatus.FAILED:
        return None

    for step_idx, step in enumerate(solution.problem.steps):
        regulated_schedule.set(
            step['train'],
            step['zone'],
            (solution.arrivals[step_idx], solution.departures[step_idx]))

    return regulated_schedule
