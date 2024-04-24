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
                self.arrivals[i] == self.departures[step['prev']]
                - step['overlap']
            )


def _add_enforce_order_constraints(
        self,
        model: cp_model.CpModel
) -> None:
    for i, step in enumerate(self.steps):
        for j, other in enumerate(self.steps):
            if (
                step['min_arrival'] < other['min_arrival']
                and step['zone'] == other['zone']
            ):
                model.Add(self.arrivals[i] < self.arrivals[j])
