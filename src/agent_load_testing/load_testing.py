from typing import List, Callable
from itertools import product
import time
import pandas as pd
from tqdm.auto import tqdm

from rlway_cpagent.regulation_solver import CpRegulationSolver


def matrix_load_testing(
        solvers: List[CpRegulationSolver],
        generator: Callable,
        ranges: dict) -> pd.DataFrame:

    data = []

    for problem_size in tqdm(product(*ranges.values())):
        problem = generator(**dict(zip(ranges.keys(), problem_size)))
        solver_computation_times = []
        for solver in solvers:
            start_time = time.time()
            solver.solve(problem)
            computation_time = time.time() - start_time
            solver_computation_times.append(computation_time)
        data.append((*problem_size, *solver_computation_times))

    df = pd.DataFrame(
        data=data,
        columns=list(ranges.keys())
        + [solver.solver_name for solver in solvers])

    return df


def linear_load_testing(
        solvers: List[CpRegulationSolver],
        generator: Callable,
        ranges: dict) -> pd.DataFrame:

    data = []

    nominal_size = {
        parameter: values["nominal"] for parameter, values in ranges.items()}
    problem_sizes = [
        {
            **nominal_size,
            parameter_name: size
        }
        for parameter_name, values in ranges.items()
        for size in values['range']
    ]

    for problem_size in problem_sizes:
        problem = generator(**problem_size)
        solver_computation_times = []
        for solver in solvers:
            start_time = time.time()
            solver.solve(problem)
            computation_time = time.time() - start_time
            solver_computation_times.append(computation_time)
        data.append((*problem_size.values(), *solver_computation_times))

    df = pd.DataFrame(
        data=data,
        columns=list(ranges.keys())
        + [solver.solver_name for solver in solvers])

    return df


def load_testing(
        solvers: List[CpRegulationSolver],
        generator: Callable,
        sizes: List[dict],
        output_path: str = None) -> pd.DataFrame:

    df = pd.DataFrame([], columns=list(sizes[0].keys()) +
                      [solver.solver_name for solver in solvers],
                      dtype=object)
    if output_path is not None:
        df.to_csv(output_path, mode='w', index=False)

    for i, problem_size in enumerate(sizes):
        problem = generator(**problem_size)
        solver_computation_times = []
        for solver in solvers:
            start_time = time.time()
            solver.solve(problem)
            computation_time = time.time() - start_time
            solver_computation_times.append(computation_time)
        df.loc[i] = (*problem_size.values(), *solver_computation_times)
        if output_path is not None:
            df.to_csv(output_path, mode='w', index=False)

    return df
