"""
Provides a rlway agent using a constraint programming solver
"""

from typing import Any, Dict, List

from rlway.pyosrd.osrd import OSRD
from rlway.pyosrd.agents import Agent

from rlway_cpagent.minizinc_agent.minizinc_solver import (
    MinizincRegulationSolver,
)
from rlway_cpagent.osrd_adapter import (
    regulation_problem_from_osrd,
    osrd_stops_from_solution,
)

SOLVER = "gecode"
SOLVER_TIMEOUT = 30


class MinizincAgent(Agent):
    """
    A regulation agent using a constraint programming solver
    """

    def stops(self, osrd: OSRD) -> List[Dict[str, Any]]:
        return self._solve_cp_problem(osrd)

    def _solve_cp_problem(self, osrd: OSRD):
        """Solve a regulation problem
        """
        problem = regulation_problem_from_osrd(osrd)
        solver = MinizincRegulationSolver("minizinc", SOLVER, SOLVER_TIMEOUT)
        solution = solver.solve(problem)
        return osrd_stops_from_solution(osrd, solution)
