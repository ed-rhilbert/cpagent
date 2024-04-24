"""
Provides a rlway agent using a constraint programming solver
"""

import pandas as pd

from pyosrd.agents.scheduler_agent import SchedulerAgent

from cpagent.ortools_agent.ortools_solver import (
    OrtoolsRegulationSolver,
)
from cpagent.osrd_adapter import (
    extra_delays_from_regulated,
)

SOLVER_TIMEOUT = 30


class OrtoolsAgent(SchedulerAgent):
    """
    A regulation agent using a constraint programming solver
    """

    allow_change_order = True
    extra_delays = None

    @property
    def steps_extra_delays(self) -> pd.DataFrame:
        self.solve()

        return self.extra_delays

    def solve(self):
        solver = OrtoolsRegulationSolver(
            "ortools",
            SOLVER_TIMEOUT,
            False,
            self.allow_change_order
        )

        regulated_schedule = solver.solve(
            self.ref_schedule,
            self.delayed_schedule,
            self.step_has_fixed_duration,
            self.weights
        )

        self.extra_delays = extra_delays_from_regulated(
            self.delayed_schedule, regulated_schedule)
