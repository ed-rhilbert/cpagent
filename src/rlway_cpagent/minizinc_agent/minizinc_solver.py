"""
Implements a CpRegulationSolver using Minizinc interface
"""

from datetime import timedelta
from dataclasses import dataclass
from pkg_resources import resource_filename

from minizinc import Model, Solver, Instance, Result, Status

from rlway_cpagent.regulation_solver import (
    CpRegulationProblem,
    CpRegulationSolution,
    OptimisationStatus,
    CpRegulationSolver,
)


@dataclass
class MinizincRegulationSolver(CpRegulationSolver):
    """
    A regulation solver using minizinc interface
    """

    minizinc_solver_name: str
    max_optimisation_time: int

    status_map = {
        Status.OPTIMAL_SOLUTION: OptimisationStatus.OPTIMAL,
        Status.SATISFIED: OptimisationStatus.SUBOPTIMAL,
        Status.UNSATISFIABLE: OptimisationStatus.FAILED
    }

    def solve(self, problem: CpRegulationProblem) -> CpRegulationSolution:
        """Solve the regulation problem

        Parameters
        ----------
        problem : CpRegulationProblem
            problem to solve

        Returns
        -------
        CpRegulationSolution
            solution of the problem
        """
        model = Model(
            resource_filename("rlway_cpagent.minizinc_agent.models",
                              "zone_model.mzn"))
        solver = Solver.lookup(self.minizinc_solver_name)
        instance = Instance(solver, model)
        self._fill_instance(instance, problem)
        result = instance.solve(
            timeout=timedelta(seconds=self.max_optimisation_time))
        solution = self._get_solution_from_result(problem, result)
        return solution

    def _fill_instance(self, instance: Instance, problem: CpRegulationProblem):
        """Use the minizinc module interface to load the problem

        Parameters
        ----------
        instance : Instance
            minizinc instance
        problem : CpRegulationProblem
            problem to solve
        """
        instance["N_trains"] = problem.nb_trains
        instance["N_zones"] = problem.nb_zones
        instance["N_steps"] = len(problem.steps)
        instance["train"] = [train+1
                             for train in problem.get_train_associations()]
        instance["zone"] = [zone+1
                            for zone in problem.get_zone_associations()]
        instance["prev"] = [prev+1
                            for prev in problem.get_prev_associations()]
        instance["min_arrival"] = problem.get_min_arrivals()
        instance["min_departure"] = problem.get_min_departures()
        instance["min_duration"] = problem.get_min_durations()
        instance["is_fixed"] = problem.get_is_fixed()
        instance["active_zones"] = \
            set([zone+1 for zone in problem.get_zone_associations()])

    def _get_solution_from_result(
            self,
            problem: CpRegulationProblem,
            result: Result) -> CpRegulationSolution:
        """builds a solution from a minizinc result

        Parameters
        ----------
        problem : CpRegulationProblem
            problem solved by the solver
        result : Result
            minizinc result

        Returns
        -------
        CpRegulationSolution
            solution to the problem
        """
        status = MinizincRegulationSolver.status_map.get(
            result.status, OptimisationStatus.FAILED)
        if status == OptimisationStatus.FAILED:
            return CpRegulationSolution(problem, status, None, None, None)

        return CpRegulationSolution(
            problem, status, result.objective,
            result["arrival"], result["departure"])
