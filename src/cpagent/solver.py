"""
Implements a OrtoolsRegulationSolver using Ortools solver
"""

import pandas as pd

from ortools.sat.python import cp_model
from pyosrd.schedules import Schedule

from cpagent.schedule_adapters import (
    steps_from_schedule,
    schedule_from_solution,
    OptimisationStatus
)


def _solve(
    self,
    ref_schedule: Schedule,
    delayed_schedule: Schedule,
    fixed_durations: pd.DataFrame = None,
    weights: pd.DataFrame = None
) -> Schedule:
    """Solves a cp regulation problem using the solver CP-SAT of ortools

    Parameters
    ----------

    Returns
    -------
    Schedule
        the refulated schedule
    """

    solver, status = self._solve_from_steps(
        len(ref_schedule.zones),
        len(ref_schedule.trains),
        steps_from_schedule(ref_schedule, delayed_schedule,
                            fixed_durations, weights)
    )
    return self._get_solution(solver, status, ref_schedule, delayed_schedule)


def _solve_from_steps(
    self,
    nb_zones,
    nb_trains,
    steps
):
    self.nb_zones = nb_zones
    self.nb_trains = nb_trains
    self.steps = steps

    model = cp_model.CpModel()
    self.history = []
    self._create_variables(model)
    self._create_constraints(model)
    self._create_objective(model)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = self.max_optimization_time
    status = solver.Solve(
        model, HistoryHandler(self) if self.save_history else None)
    return solver, status


def _get_solution(
    self,
    solver: cp_model.CpSolver,
    ortoos_status,
    ref_schedule: Schedule,
    delayed_schedule: Schedule,
) -> Schedule:
    """Generates a CpRegulationSolution from a ortools solver

    Parameters
    ----------
    solver : cp_model.CpSolver
        the ortools solver

    Returns
    -------
    Schedule
        result regulated schedule or the delayed
        schedule if optimization failed
    """
    status = self.status_map.get(
        ortoos_status, OptimisationStatus.FAILED)
    if status == OptimisationStatus.FAILED:
        return delayed_schedule

    return schedule_from_solution(
        ref_schedule,
        status,
        self.steps,
        solver.Values(self.t_in).to_list(),
        solver.Values(self.t_out).to_list())


class HistoryHandler(cp_model.CpSolverSolutionCallback):

    def __init__(self, solver):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.solver = solver

    def on_solution_callback(self):
        """Called each time a new best solution is found by the solver
        """
        self.solver.history.append(
            (
                self.UserTime(),
                self.ObjectiveValue(),
                self.BestObjectiveBound()
            )
        )
