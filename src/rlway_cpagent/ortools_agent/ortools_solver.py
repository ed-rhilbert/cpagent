"""
Implements a CpRegulationSolver using Ortools solver
"""

from ortools.sat.python import cp_model

from rlway_cpagent.regulation_solver import (
    CpRegulationProblem,
    CpRegulationSolution,
    OptimisationStatus,
    CpRegulationSolver,
)


class OrtoolsRegulationSolver(CpRegulationSolver):
    """
    Solve a regulation problem using ortools
    """

    status_map = {
        cp_model.OPTIMAL: OptimisationStatus.OPTIMAL,
        cp_model.FEASIBLE: OptimisationStatus.SUBOPTIMAL,
        cp_model.INFEASIBLE: OptimisationStatus.FAILED
    }

    def __init__(self, solver_name: str, max_optimization_time: int) -> None:
        super().__init__(solver_name)
        self.max_optimization_time = max_optimization_time
        self.arrivals = None
        self.departures = None
        self.durations = None
        self.intervals = None

    def solve(self, problem: CpRegulationProblem) -> CpRegulationSolution:
        """Solves a cp regulation problem using the solver CP-SAT of ortools

        Parameters
        ----------
        problem : CpRegulationProblem
            the problem to solve

        Returns
        -------
        CpRegulationSolution
            the solution to the problem
        """
        model = cp_model.CpModel()
        self._create_variables(model, problem)
        self._create_constraints(model, problem)
        self._create_objective(model, problem)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.max_optimization_time
        status = solver.Solve(model)
        return self._get_solution(solver, status, problem)

    def _create_variables(
            self,
            model: cp_model.CpModel,
            problem: CpRegulationProblem) -> None:
        """Create the set of decision variables

        Parameters
        ----------
        model : cp_model.CpModel
            The model to fill
        problem : CpRegulationProblem
            The problem to solve
        """
        self.arrivals = [
            model.NewIntVar(
                step['min_arrival'],
                step['min_arrival'] if step['prev'] == -1
                else cp_model.INT32_MAX,
                f"arrivals[{i}]")
            for i, step in enumerate(problem.steps)]
        self.departures = [
            model.NewIntVar(
                step['min_departure'],
                cp_model.INT32_MAX,
                f"departures[{i}]")
            for i, step in enumerate(problem.steps)]
        self.durations = [
            model.NewIntVar(
                step['min_duration'],
                step['min_duration'] if step['is_fixed']
                else cp_model.INT32_MAX,
                f"durations[{i}]")
            for i, step in enumerate(problem.steps)]
        self.intervals = [
            model.NewIntervalVar(
                self.arrivals[i],
                self.durations[i],
                self.departures[i],
                f"departures[{i}]")
            for i, step in enumerate(problem.steps)]

    def _create_constraints(
            self,
            model: cp_model.CpModel,
            problem: CpRegulationProblem) -> None:
        """Add constraints to the cp_model

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        problem : CpRegulationProblem
            problem to solve
        """
        self._add_spacing_constraints(model, problem)
        self._add_chaining_constraints(model, problem)

    def _add_spacing_constraints(
            self,
            model: cp_model.CpModel,
            problem: CpRegulationProblem) -> None:
        """Ensures that trains don't collide

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        problem : CpRegulationProblem
            problem to solve
        """
        for zone_idx in range(problem.nb_zones):
            model.AddNoOverlap([
                self.intervals[i]
                for i, step in enumerate(problem.steps)
                if step['zone'] == zone_idx
            ])

    def _add_chaining_constraints(
            self,
            model: cp_model.CpModel,
            problem: CpRegulationProblem) -> None:
        """Ensures that the departure time of a step is equal
        to the arrival time of the next one

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        problem : CpRegulationProblem
            problem to solve
        """
        for i, step in enumerate(problem.steps):
            if step['prev'] != -1:
                model.Add(self.arrivals[i] == self.departures[step['prev']])

    def _create_objective(
            self,
            model: cp_model.CpModel,
            problem: CpRegulationProblem) -> None:
        """Add the objective function to the problem

        Parameters
        ----------
        model : cp_model.CpModel
            model to fill
        problem : CpRegulationProblem
            problem to solve
        """
        model.Minimize(sum([
            self.departures[i] - step['min_departure']
            for i, step in enumerate(problem.steps)
        ]))

    def _get_solution(
            self,
            solver: cp_model.CpSolver,
            ortoos_status,
            problem: CpRegulationProblem) -> CpRegulationSolution:
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
            return CpRegulationSolution(problem, status, None, None, None)

        return CpRegulationSolution(
            problem,
            status,
            int(solver.ObjectiveValue()),
            solver.Values(self.arrivals).to_list(),
            solver.Values(self.departures).to_list())
