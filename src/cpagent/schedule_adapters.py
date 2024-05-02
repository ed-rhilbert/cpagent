"""
Provides adapting function transforming a regulation problem
from an osrd format to a constraint programming format
"""
from enum import Enum

import copy
import pandas as pd
from pyosrd.schedules import Schedule


class OptimisationStatus(Enum):
    """
    Enum representing the status of an optimisation
    """
    OPTIMAL = 1
    SUBOPTIMAL = 2
    FAILED = 3


def build_step(idx: int, train: str, zone: int, prev_idx: int, min_t_in: int,
               min_t_out: int, min_duration: int, is_fixed: bool,
               ponderation: int = 1, overlap: int = 0, next: int = -1) -> dict:
    """Add a step to the regulation problem

    Parameters
    ----------
    idx : int
        the index of this step
    train : str
        label of the associated train
    zone : int
        index of the associated zone
    prev_idx : int
        index of the previous step
    min_t_in : int
        min arrival time of the step
    min_t_out : int
        min departure time of the step
    min_duration : int
        min duration of the step
    is_fixed : bool
        true if the arrival time must match the min_t_in
    ponderation : float
        The step ponderation in the objective function
    overlap : int
        The overlap duration for this step
    next : int
        index of the next step
    """
    return {
        "idx": idx,
        "train": train,
        "zone": zone,
        "prev": prev_idx,
        "next": next,
        "min_t_in": min_t_in,
        "min_t_out": min_t_out,
        "min_duration": min_duration,
        "is_fixed": is_fixed,
        "ponderation": ponderation,
        "overlap": overlap
    }


def steps_from_schedule(
    ref_schedule: Schedule,
    delayed_schedule: Schedule,
    fixed_durations: pd.DataFrame = None,
    weights: pd.DataFrame = None
) -> list[dict]:
    """Convert a problem from a schedule format to a steps

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
    list[dict]
        A list of steps where information is stored in dictionnary
    """
    zones = ref_schedule.zones
    trains = ref_schedule.trains

    delayed_starts = delayed_schedule.starts
    delayed_ends = delayed_schedule.ends
    min_times = delayed_schedule.min_durations

    steps = []

    global_idx = 0
    for train_idx, train in enumerate(trains):
        prev_step = -1
        prev_zone = None
        for zone in ref_schedule.path(train):
            overlap = 0
            if prev_zone is not None:
                overlap = max(0, int(delayed_ends.loc[prev_zone][train]
                              - delayed_starts.loc[zone][train]))
            is_fixed = (
                True
                if (fixed_durations is not None
                    and fixed_durations.loc[zone, train_idx])
                else False
            )
            ponderation = (
                1
                if weights is None
                else weights.loc[zone][train]
            )

            if prev_step >= 0:
                steps[prev_step]["next"] = global_idx

            steps.append(build_step(
                idx=global_idx,
                train=train,
                zone=zones.index(zone),
                prev_idx=prev_step,
                min_t_in=int(delayed_starts.loc[zone][train]),
                min_t_out=int(delayed_ends.loc[zone][train]),
                min_duration=int(min_times.loc[zone][train]),
                is_fixed=is_fixed,
                ponderation=ponderation,
                overlap=overlap
            ))
            prev_zone = zone
            prev_step = len(steps) - 1
            global_idx = global_idx + 1

    return steps


def schedule_from_solution(
        ref_schedule: Schedule,
        status: OptimisationStatus,
        steps: list[dict],
        t_in: list[int],
        t_out: list[int]) -> Schedule:
    """Generate a regulated Schedule from cp results

    Parameters
    ----------
    ref_schedule : Schedule
        ref schedule
    status : OptimisationStatus
        cp status of the optimize
    steps : list[dict]
        the list of steps
    t_in : list[int]
        time of t_in
    t_out : list[int]
        time of t_out

    Returns
    -------
    Schedule
        regulated schedule
    """
    regulated_schedule = copy.deepcopy(ref_schedule)
    zones = regulated_schedule.zones

    if status == OptimisationStatus.FAILED:
        return None

    for step_idx, step in enumerate(steps):
        regulated_schedule.set(
            step['train'],
            zones[step['zone']],
            (t_in[step_idx], t_out[step_idx]))

    return regulated_schedule
