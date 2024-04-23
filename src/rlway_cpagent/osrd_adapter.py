"""
Provides adapting function transforming a regulation problem
from an osrd format to a constraint programming format
"""
from enum import Enum

from typing import Dict, List
import copy
import pandas as pd

from pyosrd.osrd import OSRD
from pyosrd.schedules import Schedule, schedule_from_osrd


class OptimisationStatus(Enum):
    """
    Enum representing the status of an optimisation
    """
    OPTIMAL = 1
    SUBOPTIMAL = 2
    FAILED = 3


def build_step(train: str, zone: int, prev_idx: int, min_arrival: int,
               min_departure: int, min_duration: int, is_fixed: bool,
               ponderation: int = 1, overlap: int = 0) -> Dict:
    """Add a step to the regulation problem

    Parameters
    ----------
    train : str
        label of the associated train
    zone : int
        index of the associated zone
    prev_idx : int
        index of the previous step
    min_arrival : int
        min arrival time of the step
    min_departure : int
        min departure time of the step
    min_duration : int
        min duration of the step
    is_fixed : bool
        true if the arrival time must match the min_arrival
    ponderation : float
        The step ponderation in the objective function
    """
    return {
        "train": train,
        "zone": zone,
        "prev": prev_idx,
        "min_arrival": min_arrival,
        "min_departure": min_departure,
        "min_duration": min_duration,
        "is_fixed": is_fixed,
        "ponderation": ponderation,
        "overlap": overlap
    }


def steps_from_osrd(
    osrd: OSRD,
    fixed_durations: pd.DataFrame = None,
    weights: pd.DataFrame = None
) -> List[Dict]:
    ref_schedule = schedule_from_osrd(osrd)
    delayed_schedule = schedule_from_osrd(osrd.delayed())

    if fixed_durations is None:
        fixed_durations = pd.DataFrame()
        trains = ref_schedule.trains
        for train_idx, _ in enumerate(trains):
            for zone in ref_schedule.trajectory(train_idx):
                fixed_durations.loc[zone, train_idx] = (
                    True
                    if osrd.stop_positions[train_idx][zone]['offset'] is None
                    else False
                )

    return steps_from_schedule(
        ref_schedule,
        delayed_schedule,
        fixed_durations,
        weights
    )


def steps_from_schedule(
    ref_schedule: Schedule,
    delayed_schedule: Schedule,
    fixed_durations: pd.DataFrame = None,
    weights: pd.DataFrame = None
) -> List[Dict]:
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
    List[Dict]
        A list of steps where information is stored in dictionnary
    """
    zones = ref_schedule.zones
    trains = ref_schedule.trains

    starts = ref_schedule.starts
    ends = ref_schedule.ends

    delayed_starts = delayed_schedule.starts
    delayed_ends = delayed_schedule.ends

    steps = []

    for train_idx, train in enumerate(trains):
        prev_step = -1
        prev_zone = None
        for zone in ref_schedule.trajectory(train_idx):
            overlap = 0
            if prev_zone is not None:
                overlap = max(0, int(delayed_ends.loc[prev_zone][train]
                              - delayed_starts.loc[zone][train]))
            is_fixed = (
                True
                if (fixed_durations is not None
                    and fixed_durations.loc[zone][train_idx])
                else False
            )
            ponderation = (
                1
                if weights is None
                else weights.loc[zone][train]
            )

            steps.append(build_step(
                train=train,
                zone=zones.index(zone),
                prev_idx=prev_step,
                min_arrival=int(starts.loc[zone][train]),
                min_departure=int(ends.loc[zone][train]),
                min_duration=int(delayed_ends.loc[zone][train])
                - int(delayed_starts.loc[zone][train]),
                is_fixed=is_fixed,
                ponderation=ponderation,
                overlap=overlap
            ))
            prev_zone = zone
            prev_step = len(steps) - 1

    return steps


def schedule_from_solution(
        ref_schedule: Schedule,
        status: OptimisationStatus,
        steps: List[Dict],
        arrivals: List[int],
        departures: List[int]) -> Schedule:
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
    zones = regulated_schedule.zones

    if status == OptimisationStatus.FAILED:
        return None

    for step_idx, step in enumerate(steps):
        regulated_schedule.set(
            step['train'],
            zones[step['zone']],
            (arrivals[step_idx], departures[step_idx]))

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
    if regulated_schedule is None:
        extra_delays = delayed_schedule.durations * -1
    else:
        extra_delays = (
            regulated_schedule.durations
            - delayed_schedule.durations
        )
    extra_delays = extra_delays.fillna(0).astype(int)
    return extra_delays
