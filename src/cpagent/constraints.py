from ortools.sat.python import cp_model


def _create_constraints(
        self,
        model: cp_model.CpModel) -> None:
    """Add constraints to the cp_model

    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """
    self._add_spacing_constraints(model)
    self._add_chaining_constraints(model)
    if not self.allow_change_order:
        self._add_enforce_order_constraints(model)


def _add_spacing_constraints(
        self,
        model: cp_model.CpModel) -> None:
    """Ensures that trains don't collide

    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """
    for zone_idx in range(self.nb_zones):
        model.AddNoOverlap([
            self.intervals[i]
            for i, step in enumerate(self.steps)
            if step['zone'] == zone_idx
        ])


def _add_chaining_constraints(
        self,
        model: cp_model.CpModel) -> None:
    """Ensures that the departure time of a step is equal
    to the arrival time of the next one

    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """
    for i, step in enumerate(self.steps):
        if step['prev'] != -1:
            model.Add(
                self.t_in[i] == self.t_out[step['prev']]
                - step['overlap']
            )


def _add_enforce_order_constraints(
        self,
        model: cp_model.CpModel
) -> None:
    for i, step in enumerate(self.steps):
        for j, other in enumerate(self.steps):
            if (
                step['min_t_in'] < other['min_t_in']
                and step['zone'] == other['zone']
            ):
                model.Add(self.t_in[i] < self.t_in[j])
