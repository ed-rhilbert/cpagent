from copy import deepcopy


from rlway_cpagent.osrd_adapter import (
    build_step,
    steps_from_osrd,
    steps_from_schedule,
    schedule_from_solution,
    OptimisationStatus,
)


def test_regulation_problem_from_osrd(osrd_point_switch):
    """Testing convertion from osrd to cp problem
    """
    steps = steps_from_osrd(osrd_point_switch)

    oracle_steps = []

    oracle_steps.append(build_step(0, 0, -1, 0, 242, 642, False, 1, 0))
    oracle_steps.append(build_step(0, 1, 0, 236, 247, 11, True, 1, 5))
    oracle_steps.append(build_step(0, 2, 1, 242, 450, 208, True, 1, 5))
    oracle_steps.append(build_step(1, 3, -1, 100, 342, 242, False, 1, 0))
    oracle_steps.append(build_step(1, 1, 3, 336, 347, 11, True, 1, 5))
    oracle_steps.append(build_step(1, 0, 4, 342, 550, 208, True, 1, 5))

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
