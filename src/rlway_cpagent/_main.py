""" Main launching functions and mechanisms
"""

from rlway.pyosrd.osrd import OSRD
from rlway.schedules import schedule_from_osrd

from rlway_cpagent.cp_agent import CPAgent
from rlway_cpagent.regulation_solver import *
from rlway_cpagent.osrd_adapter import *
from rlway_cpagent.utils import *

def main():
    """
    rlway_cpagent main launch function used as an entry point
    """
    problem = CpRegulationProblem(nb_trains=2, nb_zones=4)

    problem.add_step(1, 1, 0, 0, 10, 20, False)
    problem.add_step(1, 3, 1, 10, 20, 10, True)
    problem.add_step(1, 4, 2, 20, 30, 10, False)

    problem.add_step(2, 2, 0, 20, 30, 10, False)
    problem.add_step(2, 3, 4, 30, 40, 10, True)
    problem.add_step(2, 4, 5, 40, 50, 10, False)
    
    solution = CpRegulationSolution(
        problem, 
        OptimisationStatus.OPTIMAL,
        [0, 20, 30, 10, 20, 30],
        [20, 30, 40, 20, 30, 40])
    check_spacing(solution)
