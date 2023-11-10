from agent_load_testing.use_case_generator import generate_use_case, generate_garage_use_case
from rlway_cpagent.osrd_adapter import regulation_problem_from_schedule, schedule_from_solution
from rlway_cpagent.ortools_agent.ortools_solver import OrtoolsRegulationSolver

ref_schedule, delayed_schedule = generate_garage_use_case(2, 4, 0)
cp_problem = regulation_problem_from_schedule(ref_schedule, delayed_schedule)
solver = OrtoolsRegulationSolver()
solution = solver.solve(cp_problem)
regulated_schedule = schedule_from_solution(solution)
regulated_schedule.plot()