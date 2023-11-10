from itertools import product
import time

from rlway_cpagent.osrd_adapter import regulation_problem_from_schedule, schedule_from_solution
from rlway_cpagent.regulation_solver import CpRegulationSolver

from tqdm.auto import tqdm


def load_testing(
        solver: CpRegulationSolver,
        generator,
        max_nb_stations: int,
        max_nb_trains: int):

    nb_stations_instances = list(range(1, max_nb_stations + 1))
    nb_trains_instances = list(range(1, max_nb_trains + 1))

    performances = []

    for nb_stations, nb_trains in tqdm(product(nb_stations_instances, nb_trains_instances)):
        ref_schedule, delayed_schedule = generator(nb_stations, nb_trains)
        problem = regulation_problem_from_schedule(ref_schedule, delayed_schedule)
        start_time = time.time()
        solver.solve(problem)
        end_time = time.time() - start_time
        performances.append((nb_stations, nb_trains, end_time))
    return performances
