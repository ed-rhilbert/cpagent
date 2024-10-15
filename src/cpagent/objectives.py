from ortools.sat.python import cp_model


def _create_objective(
    self,
    model: cp_model.CpModel
) -> None:
    """Add the objective function to the problem

    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """
    model.Minimize(sum([
        (self.t_in[i] - step['min_t_in'])
        * step['ponderation']
        +
        ((self.t_out[i] - step['min_t_out'])
            * step['ponderation'] if self.penalize_t_out else 0.)
        for i, step in enumerate(self.steps)
    ]))
