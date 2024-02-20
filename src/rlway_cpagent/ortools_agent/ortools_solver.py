"""
Implements a OrtoolsRegulationSolver using Ortools solver
"""

from ortools.sat.python import cp_model
import pandas as pd

from rlway.schedules import Schedule

from rlway_cpagent.osrd_adapter import (
    steps_from_schedule,
    schedule_from_solution,
    OptimisationStatus
)


class OrtoolsRegulationSolver:
    """
    Solve a regulation problem using ortools
    """

    status_map = {
        cp_model.OPTIMAL: OptimisationStatus.OPTIMAL,
        cp_model.FEASIBLE: OptimisationStatus.SUBOPTIMAL,
        cp_model.INFEASIBLE: OptimisationStatus.FAILED
    }

    def __init__(
            self,
            solver_name: str,
            max_optimization_time: int,
            save_history: bool = False,
            allow_change_order: bool = True) -> None:
        self.solver_name = solver_name
        self.max_optimization_time = max_optimization_time
        self.save_history = save_history
        self.allow_change_order = allow_change_order
        self.arrivals = None
        self.departures = None
        self.durations = None
        self.intervals = None
        self.history = None

    def solve(
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
        CpRegulationSolution
            the solution to the problem
        """

        solver, status = self.solve_from_steps(
            len(ref_schedule.blocks),
            len(ref_schedule.trains),
            steps_from_schedule(ref_schedule, delayed_schedule,
                                fixed_durations, weights)
        )
        return self._get_solution(solver, status, ref_schedule)

    def solve_from_steps(
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

    def _create_variables(
            self,
            model: cp_model.CpModel) -> None:
        """Create the set of decision variables

        Parameters
        ----------
        model : cp_model.CpModel
            The model to fill
        """
        self.arrivals = [
            model.NewIntVar(
                step['min_arrival'],
                step['min_arrival'] if step['prev'] == -1
                else cp_model.INT32_MAX,
                f"arrivals[{i}]")
            for i, step in enumerate(self.steps)]
        self.departures = [
            model.NewIntVar(
                step['min_departure'],
                cp_model.INT32_MAX,
                f"departures[{i}]")
            for i, step in enumerate(self.steps)]
        self.durations = [
            model.NewIntVar(
                step['min_duration'],
                step['min_duration'] if step['is_fixed']
                else cp_model.INT32_MAX,
                f"durations[{i}]")
            for i, step in enumerate(self.steps)]
        self.intervals = [
            model.NewIntervalVar(
                self.arrivals[i],
                self.durations[i],
                self.departures[i],
                f"departures[{i}]")
            for i, step in enumerate(self.steps)]

    def _create_constraints(
            self,
            model: cp_model.CpModel) -> None:
        """Add constraints to the cp_model

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        """
        self._add_spacing_constraints(model)
        self._add_chaining_constraints(model)
        if not self.allow_change_order:
            self._add_enforce_order_constraints(model)

    def _add_spacing_constraints(
            self,
            model: cp_model.CpModel) -> None:
        """Ensures that trains don't collide

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        """
        for zone_idx in range(self.nb_zones):
            model.AddNoOverlap([
                self.intervals[i]
                for i, step in enumerate(self.steps)
                if step['zone'] == zone_idx
            ])

    def _add_chaining_constraints(
            self,
            model: cp_model.CpModel) -> None:
        """Ensures that the departure time of a step is equal
        to the arrival time of the next one

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        """
        for i, step in enumerate(self.steps):
            if step['prev'] != -1:
                model.Add(self.arrivals[i] == self.departures[step['prev']]
                          - step['overlap'])

    def _add_enforce_order_constraints(
            self,
            model: cp_model.CpModel
    ) -> None:
        for i, step in enumerate(self.steps):
            for j, other in enumerate(self.steps):
                if (
                    step['min_arrival'] < other['min_arrival']
                    and step['zone'] == other['zone']
                ):
                    model.Add(self.arrivals[i] < self.arrivals[j])

    def _create_objective(
        self,
        model: cp_model.CpModel
    ) -> None:
        """Add the objective function to the problem

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        """
        model.Minimize(sum([
            (self.arrivals[i] - step['min_arrival'])
            * step['ponderation']
            for i, step in enumerate(self.steps)
        ]))

    def _get_solution(
        self,
        solver: cp_model.CpSolver,
        ortoos_status,
        ref_schedule: Schedule,
    ) -> Schedule:
        """Generates a CpRegulationSolution from a ortools solver

        Parameters
        ----------
        solver : cp_model.CpSolver
            the ortools solver

        Returns
        -------
        CpRegulationSolution
            result solution
        """
        status = OrtoolsRegulationSolver.status_map.get(
            ortoos_status, OptimisationStatus.FAILED)
        if status == OptimisationStatus.FAILED:
            return None

        return schedule_from_solution(
            ref_schedule,
            status,
            self.steps,
            solver.Values(self.arrivals).to_list(),
            solver.Values(self.departures).to_list())


class HistoryHandler(cp_model.CpSolverSolutionCallback):

    def __init__(self, solver: OrtoolsRegulationSolver):
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
