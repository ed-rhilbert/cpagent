from agent_load_testing.use_case_generator import generate_garage_use_case
from agent_load_testing.load_testing import linear_load_testing

from rlway_cpagent.minizinc_agent.minizinc_solver import MinizincRegulationSolver
from rlway_cpagent.ortools_agent.ortools_solver import OrtoolsRegulationSolver

def main():
    linear_load_testing(
        [OrtoolsRegulationSolver("ortools", 10)],
        generate_garage_use_case,
        {
            "nb_stations": {
                "range": range(1, 5),
                "nominal": 3
            },
            "nb_trains": {
                "range": range(1, 5),
                "nominal": 3
            }
        })


if __name__ == "__main__":
    main()
