from agent_load_testing.use_case_generator import generate_garage_use_case
from rlway_cpagent.osrd_adapter import regulation_problem_from_schedule, schedule_from_solution
from rlway_cpagent.ortools_agent.ortools_solver import OrtoolsRegulationSolver
from rlway_cpagent.minizinc_agent.minizinc_solver import MinizincRegulationSolver
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from agent_load_testing.load_testing import matrix_load_testing, linear_load_testing

performances_df = pd.read_csv("./docs/load_testing/table.csv")
print(performances_df.to_latex(index=False, float_format="%.2f"))