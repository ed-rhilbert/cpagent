"""
Provides a rlway agent using a constraint programming solver
"""

from ortools.sat.python import cp_model
from pyosrd.agents.scheduler_agent import SchedulerAgent
from pyosrd.schedules import Schedule

from cpagent.schedule_adapters import (
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
    def regulated_schedule(self) -> Schedule:
        return self.solve()

    def solve(self):
        return self._solve(
            self.ref_schedule,
            self.delayed_schedule,
            self.step_has_fixed_duration,
            self.weights
        )
