"""
Provides adapting function transforming a regulation problem
from an osrd format to a constraint programming format
"""

from typing import Any, Dict, List
import copy
import pandas as pd

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
        prev_zone = None
        for zone in ref_schedule.trajectory(train_idx):
            overlap = 0
            if prev_zone is not None:
                overlap = max(0, int(delayed_ends.loc[prev_zone][train_idx]
                              - delayed_starts.loc[zone][train_idx]))
            problem.add_step(
                train=train_idx,
                zone=zones.index(zone),
                prev_idx=prev_step,
                min_arrival=int(starts.loc[zone][train_idx]),
                min_departure=int(ends.loc[zone][train_idx]),
                min_duration=int(delayed_ends.loc[zone][train_idx])
                - int(delayed_starts.loc[zone][train_idx]),
                is_fixed=True if osrd.stop_positions[train_idx][zone]['offset']
                is None else False,
                overlap=overlap
            )
            prev_zone = zone
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
        ref_schedule: Schedule,
        delayed_schedule: Schedule,
        fixed_durations: pd.DataFrame,
        weights: pd.DataFrame) -> CpRegulationProblem:
    """Convert a problem from a schedule format to a CpRegulationProblem

    Parameters
    ----------
    ref_schedule : Schedule
        reference Schedule
    delayed_schedule : Schedule
        delayed Schedule
    fixed_durations : pd.DataFrame
        steps that are fixed
    weights : pd.DataFrame
        weight for each step

    Returns
    -------
    CpRegulationProblem
        problem in a CpRegulationProblem format
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
        prev_zone = None
        for zone in ref_schedule.trajectory(train_idx):
            overlap = 0
            if prev_zone is not None:
                overlap = max(0, int(delayed_ends.loc[prev_zone][train_idx]
                              - delayed_starts.loc[zone][train_idx]))
            problem.add_step(
                train=train_idx,
                zone=zones.index(zone),
                prev_idx=prev_step,
                min_arrival=int(starts.loc[zone][train_idx]),
                min_departure=int(ends.loc[zone][train_idx]),
                min_duration=int(delayed_ends.loc[zone][train_idx])
                - int(delayed_starts.loc[zone][train_idx]),
                is_fixed=fixed_durations.loc[zone][train_idx],
                ponderation=int(weights.loc[zone][train_idx]),
                overlap=overlap
            )
            prev_zone = zone
            prev_step = len(problem.steps) - 1

    return problem


def schedule_from_solution(
        ref_schedule: Schedule,
        solution: CpRegulationSolution) -> Schedule:
    """Generate a regulated Schedule from a CpRegulationSolution

    Parameters
    ----------
    ref_schedule : Schedule
        ref schedule
    solution : CpRegulationSolution
        cp solution

    Returns
    -------
    Schedule
        regulated schedule
    """
    regulated_schedule = copy.deepcopy(ref_schedule)
    zones = regulated_schedule.blocks

    if solution.status == OptimisationStatus.FAILED:
        return None

    for step_idx, step in enumerate(solution.problem.steps):
        regulated_schedule.set(
            step['train'],
            zones[step['zone']],
            (solution.arrivals[step_idx], solution.departures[step_idx]))

    return regulated_schedule


def extra_delays_from_regulated(
        delayed_schedule: Schedule,
        regulated_schedule: Schedule) -> pd.DataFrame:
    """Convert from delayed and regulated schedule to extra delays

    Parameters
    ----------
    delayed_schedule : Schedule
        delayed schedule
    regulated_schedule : Schedule
        regulated schedule

    Returns
    -------
    pd.DataFrame
        extra delays
    """
    extra_delays = regulated_schedule.durations - delayed_schedule.durations
    extra_delays = extra_delays.fillna(0).astype(int)
    return extra_delays

