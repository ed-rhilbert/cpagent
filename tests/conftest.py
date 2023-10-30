"""Fixtures"""

import shutil

import pytest

from rlway.pyosrd import OSRD
from rlway_cpagent.regulation_solver import CpRegulationProblem


# ---------------------------------------------------------------------------- #
#                                OSRD use cases                                #
# ---------------------------------------------------------------------------- #


@pytest.fixture(scope='session')
def osrd_point_switch():
    """Create the simple OSRD use case 'point_switch'

    Yields
    ------
    _type_
        _description_
    """
    osrd = OSRD('tmp', 'point_switch')
    osrd.add_delay('train0', 0, 400.)
    yield osrd
    shutil.rmtree('tmp', ignore_errors=True)


# ---------------------------------------------------------------------------- #
#                         CpRegulationProblem use cases                        #
# ---------------------------------------------------------------------------- #


@pytest.fixture(scope='session')
def use_case_cp_4_zones_switch():
    """Generate CP problem with 3 zones connected by one switch

    Yields
    ------
    CpRegulationProblem
        generated problem
    """
    problem = CpRegulationProblem(nb_trains=2, nb_zones=4)

    problem.add_step(0, 0, -1, 0, 10, 20, False)
    problem.add_step(0, 2, 0, 10, 20, 10, True)
    problem.add_step(0, 3, 1, 20, 30, 10, False)

    problem.add_step(1, 1, -1, 20, 30, 10, False)
    problem.add_step(1, 2, 3, 30, 40, 10, True)
    problem.add_step(1, 3, 4, 40, 50, 10, False)

    yield problem


@pytest.fixture(scope='session')
def use_case_delay_conv():
    """Generate a use case with 2 trains circulating
    between two stations of 2 tracks connected by one track

    Yields
    ------
    _type_
        _description_
    """
    delay_at_first_departure = 0

    problem = CpRegulationProblem(nb_trains=2, nb_zones=7)

    problem.add_step(0, 0, -1, 0, 10, 10 + delay_at_first_departure, False)
    problem.add_step(0, 2, 0, 10, 20, 10, True)
    problem.add_step(0, 3, 1, 20, 30, 10, False)
    problem.add_step(0, 4, 2, 30, 40, 10, True)
    problem.add_step(0, 5, 3, 40, 50, 10, False)

    problem.add_step(1, 1, -1, 20, 30, 10, False)
    problem.add_step(1, 2, 5, 30, 40, 10, True)
    problem.add_step(1, 3, 6, 40, 50, 10, False)
    problem.add_step(1, 4, 6, 50, 60, 10, True)
    problem.add_step(1, 6, 8, 60, 70, 10, False)

    yield problem


@pytest.fixture(scope='session')
def use_case_infeasible():
    """Generate an infeasible use case
    with a straight line composed by 2 tracks

    Yields
    ------
    _type_
        _description_
    """
    problem = CpRegulationProblem(nb_trains=2, nb_zones=2)

    problem.add_step(0, 0, -1, 0, 10, 30, False)
    problem.add_step(0, 1, 0, 10, 20, 10, False)

    problem.add_step(1, 0, -1, 10, 20, 10, False)
    problem.add_step(1, 1, 0, 20, 30, 10, False)

    yield problem


@pytest.fixture(scope='session')
def use_case_straight_line_2t():
    """Generate a simple use case with a straight line of 2 tracks
    and two trains with a delay on the first train

    Yields
    ------
    _type_
        _description_
    """
    problem = CpRegulationProblem(2, 2)

    problem.add_step(0, 0, -1, 0, 10, 10, False)
    problem.add_step(0, 1, 0, 10, 20, 20, False)

    problem.add_step(1, 0, -1, 10, 20, 10, False)
    problem.add_step(1, 1, 2, 20, 30, 10, False)

    yield problem
