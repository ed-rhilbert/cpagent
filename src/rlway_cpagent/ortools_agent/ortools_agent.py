"""
Provides a rlway agent using a constraint programming solver
"""

import pandas as pd

from rlway.pyosrd.scheduler_agent import SchedulerAgent

from rlway_cpagent.ortools_agent.ortools_solver import (
    OrtoolsRegulationSolver,
)
from rlway_cpagent.osrd_adapter import (
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
        if self.extra_delays is None:
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
            self.initial_schedule,
            self.delayed_schedule,
            self.step_has_fixed_duration,
            self.weights
        )

        self.extra_delays = extra_delays_from_regulated(
            self.delayed_schedule, regulated_schedule)
