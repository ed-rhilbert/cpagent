from copy import deepcopy

import pandas as pd
from cpagent.schedule_adapters import (
    build_step,
    steps_from_schedule,
    schedule_from_solution,
    OptimisationStatus,
)

from pyosrd.osrd import OSRD
from pyosrd.schedules import schedule_from_osrd


def steps_from_osrd(
    osrd: OSRD,
    fixed_durations: pd.DataFrame = None,
    weights: pd.DataFrame = None
) -> list[dict]:
    ref_schedule = schedule_from_osrd(osrd)
    delayed_schedule = schedule_from_osrd(osrd.delayed())

    if fixed_durations is None:
        fixed_durations = pd.DataFrame()
        trains = ref_schedule.trains
        for train_idx, _ in enumerate(trains):
            for zone in ref_schedule.path(train_idx):
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


def test_regulation_problem_from_osrd(osrd_point_switch):
    """Testing convertion from osrd to cp problem
    """
    steps = steps_from_osrd(osrd_point_switch)

    oracle_steps = []

    oracle_steps.append(build_step(0, "train0", 0, -1, 400, 642, 242, False, 1, 0, 1)) # noqa
    oracle_steps.append(build_step(1, "train0", 1, 0, 636, 647, 10, True, 1, 5, 2)) # noqa
    oracle_steps.append(build_step(2, "train0", 2, 1, 642, 849, 207, True, 1, 5)) # noqa
    oracle_steps.append(build_step(3, "train1", 3, -1, 100, 342, 242, False, 1, 0, 4)) # noqa
    oracle_steps.append(build_step(4, "train1", 1, 3, 336, 347, 10, True, 1, 5, 5)) # noqa
    oracle_steps.append(build_step(5, "train1", 0, 4, 342, 549, 207, True, 1, 5)) # noqa

    assert oracle_steps == steps


def test_schedule_from_solution(schedule_straight_line_2t):
    steps = steps_from_schedule(*schedule_straight_line_2t)

    ref_schedule = schedule_straight_line_2t[0]

    regulated_schedule = schedule_from_solution(
        ref_schedule,
        OptimisationStatus.OPTIMAL,
        steps,
        [0, 10, 10, 30],
        [10, 30, 30, 40]
    )

    oracle_regulated = deepcopy(schedule_straight_line_2t[1])
    oracle_regulated.set(1, 0, [10, 30])
    oracle_regulated.set(1, 1, [30, 40])

    assert (regulated_schedule.durations
            == oracle_regulated.durations).all().all()
    assert (regulated_schedule.starts
            == oracle_regulated.starts).all().all()
    assert (regulated_schedule.ends
            == oracle_regulated.ends).all().all()
