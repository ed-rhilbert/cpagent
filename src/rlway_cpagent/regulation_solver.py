"""
Provide the definition of a constraint programming problem applied to
regulation, a CP regulation solution and a constraint programming solver
"""

from typing import Any, Dict, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from pkg_resources import resource_filename

from minizinc import Model, Solver, Instance, Result, Status


class CpRegulationProblem:
    """
    Description of a regulation problem
    """

    def __init__(self, nb_trains: int, nb_zones: int) -> None:
        self.nb_trains = nb_trains
        self.nb_zones = nb_zones
        self.steps = []

    def add_step(self, train: int, zone: int, prev_idx: int, min_arrival: int,
                 min_departure: int, min_duration: int, is_fixed: bool):
        """Add a step to the regulation problem

        Parameters
        ----------
        train : int
            index of the associated train
        zone : int
            index of the associated zone
        prev_idx : int
            index of the previous step
        min_arrival : int
            min arrival time of the step
        min_departure : int
            min departure time of the step
        min_duration : int
            min duration of the step
        is_fixed : bool
            true if the arrival time must match the min_arrival
        """
        self.steps.append({
            "train": train,
            "zone": zone,
            "prev": prev_idx,
            "min_arrival": min_arrival,
            "min_departure": min_departure,
            "min_duration": min_duration,
            "is_fixed": is_fixed
        })

    def get_train_associations(self) -> List[int]:
        """Return the list of trains associated with each step

        Returns
        -------
        List[int]
            train index
        """
        return [step['train'] for step in self.steps]

    def get_zone_associations(self) -> List[int]:
        """Return the list of zones associated with each step

        Returns
        -------
        List[int]
            zone index
        """
        return [step['zone'] for step in self.steps]

    def get_prev_associations(self) -> List[int]:
        """Return the list of zones associated with each step

        Returns
        -------
        List[int]
            previous step index
        """
        return [step['prev'] for step in self.steps]

    def get_min_arrivals(self) -> List[int]:
        """Return the list of min arrival times of each step

        Returns
        -------
        List[int]
            min arrival times
        """
        return [step['min_arrival'] for step in self.steps]

    def get_min_departures(self) -> List[int]:
        """Return the list of min departure times of each step

        Returns
        -------
        List[int]
            min departure times
        """
        return [step['min_departure'] for step in self.steps]

    def get_min_durations(self) -> List[int]:
        """Return the list of min duration time of each step

        Returns
        -------
        List[int]
            min duration time
        """
        return [step['min_duration'] for step in self.steps]

    def get_is_fixed(self) -> List[bool]:
        """Return the list of flag indicating if a step is fixed

        Returns
        -------
        List[bool]
            is_fixed flags
        """
        return [step['is_fixed'] for step in self.steps]


class OptimisationStatus(Enum):
    """
    Enum representing the status of an optimisation
    """
    OPTIMAL = 1
    SUBOPTIMAL = 2
    FAILED = 3


@dataclass
class CpRegulationSolution:
    """
    Description of a regulation solution
    """

    problem: CpRegulationProblem
    status: OptimisationStatus
    arrivals: List[int]
    departures: List[int]

    def get_delays(self) -> List[Dict[str, Any]]:
        """Return the delays applied to each steps

        Returns
        -------
        List[Dict[str, Any]]
            list of delays
        """
        if self.status == OptimisationStatus.FAILED:
            return []

        delays = []
        for idx, step in enumerate(self.problem.steps):
            duration = self.departures[idx] - self.arrivals[idx]
            delay = duration - step["min_duration"]
            if delay > 0:
                delays.append({
                    "train": step["train"],
                    "zone": step["zone"],
                    "duration": delay})
        return delays


class CpRegulationSolver(ABC):
    """
    Abstract class representing a constraint programming solver
    for the regulation problem
    """

    @abstractmethod
    def solve(self, problem: CpRegulationProblem) -> CpRegulationSolution:
        """Solve a regulation problem

        Parameters
        ----------
        problem : CpRegulationProblem
            the problem to solve

        Returns
        -------
        CpRegulationSolution
            the solution returned by the solver
        """


@dataclass
class MinizincRegulationSolver(CpRegulationSolver):
    """
    A regulation solver using minizinc interface
    """

    solver_name: str
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
            resource_filename("rlway_cpagent.models", "zone_model.mzn"))
        solver = Solver.lookup(self.solver_name)
        instance = Instance(solver, model)
        self.fill_instance(instance, problem)
        result = instance.solve(
            timeout=timedelta(seconds=self.max_optimisation_time))
        solution = self.get_solution_from_result(problem, result)
        return solution

    def fill_instance(self, instance: Instance, problem: CpRegulationProblem):
        """Use the minizinc module interface to load the problem

        Parameters
        ----------
        instance : Instance
            minizinc instance
        problem : CpRegulationProblem
            problem to solve
        """
        instance["Nb_Trains"] = problem.nb_trains
        instance["Nb_Zones"] = problem.nb_zones
        instance["Nb_Steps"] = len(problem.steps)
        instance["train"] = problem.get_train_associations()
        instance["zone"] = problem.get_zone_associations()
        instance["prev"] = problem.get_prev_associations()
        instance["min_arrival"] = problem.get_min_arrivals()
        instance["min_departure"] = problem.get_min_departures()
        instance["min_duration"] = problem.get_min_durations()
        instance["is_fixed"] = problem.get_is_fixed()

    def get_solution_from_result(
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
        status = MinizincRegulationSolver.status_map[result.status]
        if status == OptimisationStatus.FAILED:
            return CpRegulationSolution(problem, status, None, None)

        return CpRegulationSolution(
            problem, status, result["arrival"], result["departure"])
