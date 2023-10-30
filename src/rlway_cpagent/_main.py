""" Main launching functions and mechanisms
"""

from rlway.pyosrd.osrd import OSRD
from rlway.schedules import schedule_from_osrd

from rlway_cpagent.regulation_solver import CpRegulationProblem
from rlway_cpagent.ortools_agent.ortools_solver import OrtoolsRegulationSolver

def main():
    """
    rlway_cpagent main launch function used as an entry point
    """
    problem = CpRegulationProblem(nb_trains=2, nb_zones=4)

    problem.add_step(0, 0, -1, 0, 10, 20, False)
    problem.add_step(0, 2, 0, 10, 20, 10, True)
    problem.add_step(0, 3, 1, 20, 30, 10, False)

    problem.add_step(1, 1, -1, 20, 30, 10, False)
    problem.add_step(1, 2, 3, 30, 40, 10, True)
    problem.add_step(1, 3, 4, 40, 50, 10, False)
    
    solver = OrtoolsRegulationSolver()
    solver.solve(problem)
