"""
Provides adapting function transforming a regulation problem
from an osrd format to a constraint programming format
"""

from typing import Any, Dict, List

from rlway.pyosrd.osrd import OSRD
from rlway.schedules import schedule_from_osrd

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

    for train_idx in range(len(trains)):
        prev_step = 0
        for zone in ref_schedule.trajectory(train_idx):
            problem.add_step(
                train_idx + 1,
                zones.index(zone) + 1,
                prev_step,
                int(starts.loc[zone][train_idx]),
                int(ends.loc[zone][train_idx]),
                int(delayed_ends.loc[zone][train_idx])
                - int(delayed_starts.loc[zone][train_idx]),
                True if osrd.stop_positions[train_idx][zone]['offset']
                is None else False
            )
            prev_step = len(problem.steps)

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
        pos = osrd.stop_positions[delay["train"]-1][zones[delay["zone"]-1]]
        assert pos['offset'] is not None
        stops.append({
            "train": delay["train"]-1,
            "position": pos['offset'],
            "duration": delay["duration"]
        })
    return stops