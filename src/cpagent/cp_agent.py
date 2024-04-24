"""
Provides a rlway agent using a constraint programming solver
"""

import pandas as pd

from ortools.sat.python import cp_model
from pyosrd.agents.scheduler_agent import SchedulerAgent

from cpagent.osrd_adapter import (
    extra_delays_from_regulated,
)
from cpagent.osrd_adapter import (
    OptimisationStatus
)


SOLVER_TIMEOUT = 30


class CpAgent(SchedulerAgent):
    """
    A regulation agent using a constraint programming solver
    """

    from .constraints import (
        _add_spacing_constraints,
        _add_chaining_constraints,
        _add_enforce_order_constraints,
        _create_constraints  # must be last because it calls above methods
    )
    from .variables import _create_variables
    from .objectives import _create_objective
    from .solver import (
        _solve_from_steps,
        _get_solution,
        _solve
    )

    arrivals = None
    departures = None
    durations = None
    intervals = None
    history = None
    allow_change_order = True
    extra_delays = None
    max_optimization_time = SOLVER_TIMEOUT
    save_history = False

    # solution

    status_map = {
        cp_model.OPTIMAL: OptimisationStatus.OPTIMAL,
        cp_model.FEASIBLE: OptimisationStatus.SUBOPTIMAL,
        cp_model.INFEASIBLE: OptimisationStatus.FAILED
    }

    @property
    def steps_extra_delays(self) -> pd.DataFrame:
        self.solve()

        return self.extra_delays

    def solve(self):
        regulated_schedule = self._solve(
            self.ref_schedule,
            self.delayed_schedule,
            self.step_has_fixed_duration,
            self.weights
        )

        self.extra_delays = extra_delays_from_regulated(
            self.delayed_schedule, regulated_schedule)
