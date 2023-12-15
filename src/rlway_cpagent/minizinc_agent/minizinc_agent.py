"""
Provides a rlway agent using a constraint programming solver
"""

from typing import Any, Dict, List

import pandas as pd

from rlway.pyosrd.scheduler_agent import SchedulerAgent

from rlway_cpagent.minizinc_agent.minizinc_solver import (
    MinizincRegulationSolver,
)
from rlway_cpagent.osrd_adapter import (
    regulation_problem_from_schedule,
    schedule_from_solution,
    extra_delays_from_regulated,
)

SOLVER = "gecode"
SOLVER_TIMEOUT = 30


class MinizincAgent(SchedulerAgent):
    """
    A regulation agent using a Minizinc constraint programming solver
    """

    @property
    def steps_extra_delays(self) -> pd.DataFrame:
        problem = regulation_problem_from_schedule(
            self.initial_schedule,
            self.delayed_schedule,
            self.step_has_fixed_duration,
            self.weights)
        solver = MinizincRegulationSolver("minizinc", SOLVER, SOLVER_TIMEOUT)
        solution = solver.solve(problem)
        regulated_schedule = schedule_from_solution(
            self.initial_schedule, solution)
        extra_delays = extra_delays_from_regulated(
            self.delayed_schedule, regulated_schedule)
        return extra_delays
