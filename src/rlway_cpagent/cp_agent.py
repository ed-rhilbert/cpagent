"""
Provides a rlway agent using a constraint programming solver
"""

from typing import Any, Dict, List

from rlway.pyosrd.osrd import OSRD
from rlway.pyosrd.agents import Agent

from rlway_cpagent.regulation_solver import MinizincRegulationSolver
from rlway_cpagent.osrd_adapter import (
    regulation_problem_from_osrd,
    osrd_stops_from_solution,
)


class CPAgent(Agent):
    """
    A regulation agent using a constraint programming solver
    """

    def stops(self, osrd: OSRD) -> List[Dict[str, Any]]:
        return self.solve_cp_problem(osrd)

    def solve_cp_problem(self, osrd: OSRD):
        """Solve a regulation problem

        Parameters
        ----------
        osrd : OSRD
            _description_

        Returns
        -------
        _type_
            _description_
        """
        problem = regulation_problem_from_osrd(osrd)
        solver = MinizincRegulationSolver("gecode", 30)
        solution = solver.solve(problem)
        return osrd_stops_from_solution(osrd, solution)
