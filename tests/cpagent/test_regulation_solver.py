from cpagent.solution import CpRegulationSolution


def test_get_delays(use_case_straight_line_2t):
    """Testing the function get_delays of the class CpRegulationSolution
    """
    solution = CpRegulationSolution(
        use_case_straight_line_2t[0],
        use_case_straight_line_2t[1],
        use_case_straight_line_2t[2],
        0,
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
    """
    solution = CpRegulationSolution(
        use_case_straight_line_2t[0],
        use_case_straight_line_2t[1],
        use_case_straight_line_2t[2],
        0,
        None,
        None)

    delays_oracle = []

    assert solution.get_delays() == delays_oracle
