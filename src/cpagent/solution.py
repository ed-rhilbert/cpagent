from typing import Any, Dict, List
from dataclasses import dataclass

from ortools.sat.python import cp_model

from cpagent.cp_agent import CpAgent


@dataclass
class CpRegulationSolution:
    """
    Description of a regulation solution
    """

    nb_zones: int
    nb_trains: int
    steps: List[Dict]
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
        delays = []
        if (
            self.steps is None or
            self.arrivals is None or
            self.departures is None
        ):
            return delays
        for idx, step in enumerate(self.steps):
            duration = self.departures[idx] - self.arrivals[idx]
            delay = duration - step["min_duration"]
            if delay > 0:
                delays.append({
                    "train": step["train"],
                    "zone": step["zone"],
                    "duration": delay})
        return delays


def build_solution(
    solver: CpAgent,
    cp_solver: cp_model.CpSolver
) -> CpRegulationSolution:
    return CpRegulationSolution(
        solver.nb_trains,
        solver.nb_zones,
        solver.steps,
        int(cp_solver.ObjectiveValue()),
        cp_solver.Values(solver.arrivals).to_list(),
        cp_solver.Values(solver.departures).to_list()
    )
