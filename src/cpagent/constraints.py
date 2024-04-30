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
    self._add_precedence_constraints(model)


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


def _add_precedence_constraints(
        self,
        model: cp_model.CpModel
) -> None:
    # build a map of step per zone
    step_per_zone = {}
    for step in self.steps:
        if not step['zone'] in step_per_zone:
            step_per_zone[step['zone']] = []
        step_per_zone[step['zone']].append(step)

    for steps_of_zone in step_per_zone.values():
        model.AddExactlyOne(self.firsts[step['idx']] for step in steps_of_zone)
        model.AddExactlyOne(self.lasts[step['idx']] for step in steps_of_zone)

    for i, step in enumerate(self.steps):
        all_others_before = [self.lasts[i]]
        all_others_after = [self.firsts[i]]
        for j, other in enumerate(self.steps):
            if (
                step['train'] != other['train']
                and step['zone'] == other['zone']
            ):
                all_others_before.append(self.precs[i][j])
                all_others_after.append(self.precs[j][i])
                model.AddAtMostOne([self.precs[i][j], self.precs[j][i]])
                model.Add(
                    self.t_out[i]
                    + self.itinierary_setup * self.diff_itineraries[i][j]
                    <= self.t_in[j]) \
                    .OnlyEnforceIf(self.precs[i][j])

        model.AddExactlyOne(all_others_before)
        model.AddExactlyOne(all_others_after)
