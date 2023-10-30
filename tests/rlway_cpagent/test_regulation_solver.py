from rlway_cpagent.regulation_solver import (
    CpRegulationSolution,
    OptimisationStatus,
)


def test_get_delays(use_case_straight_line_2t):
    """Testing the function get_delays of the class CpRegulationSolution

    Parameters
    ----------
    use_case_straight_line_2t : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_straight_line_2t,
        OptimisationStatus.OPTIMAL,
        [0, 10, 10, 30],
        [10, 30, 30, 40])

    delays_oracle = [
        {
            "train": 1,
            "zone": 0,
            "duration": 10
        }
    ]

    assert solution.get_delays() == delays_oracle


def test_get_delays_empty(use_case_straight_line_2t):
    """Testing the function get_delays of the class CpRegulationSolution
    with an empty solution

    Parameters
    ----------
    use_case_straight_line_2t : _type_
        _description_
    """
    solution = CpRegulationSolution(
        use_case_straight_line_2t,
        OptimisationStatus.FAILED,
        None,
        None)

    delays_oracle = []

    assert solution.get_delays() == delays_oracle
