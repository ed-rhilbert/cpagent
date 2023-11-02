"""
Provide the definition of a constraint programming problem applied to
regulation, a CP regulation solution and a constraint programming solver
"""

from typing import Any, Dict, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class CpRegulationProblem:
    """
    Description of a regulation problem
    """

    def __init__(self, nb_trains: int, nb_zones: int) -> None:
        self.nb_trains = nb_trains
        self.nb_zones = nb_zones
        self.steps = []

    def add_step(self, train: int, zone: int, prev_idx: int, min_arrival: int,
                 min_departure: int, min_duration: int, is_fixed: bool,
                 ponderation: int = 1):
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
        ponderation : float
            The step ponderation in the objective function
        """
        self.steps.append({
            "train": train,
            "zone": zone,
            "prev": prev_idx,
            "min_arrival": min_arrival,
            "min_departure": min_departure,
            "min_duration": min_duration,
            "is_fixed": is_fixed,
            "ponderation": ponderation
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

    def get_ponderations(self) -> List[float]:
        """Return the ponderation of each step

        Returns
        -------
        List[float]
            List of ponderations
        """
        return [step['ponderation'] for step in self.steps]


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
    cost: float
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

    def __eq__(self, other):
        return self.cost == other.cost

    def __ne__(self, other):
        return self.cost != other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost


@dataclass
class CpRegulationSolver(ABC):
    """
    Abstract class representing a constraint programming solver
    for the regulation problem
    """
    solver_name: str

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
