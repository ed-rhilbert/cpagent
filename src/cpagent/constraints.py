from ortools.sat.python import cp_model
from collections.abc import Sequence


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
    self._add_itineraries_constraints(model)


def _add_spacing_constraints(
        self,
        model: cp_model.CpModel) -> None:
    """Ensures that trains don't collide

    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """

    # Constraint 1
    # for zone_idx in range(self.nb_zones):
    #     model.AddNoOverlap([
    #         self.intervals[i]
    #         for i, step in enumerate(self.steps)
    #         if step['zone'] == zone_idx
    #     ])


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

    # Constraint 5
    for i, step in enumerate(self.steps):
        for next_i in step["nexts"]:
            model.Add(
                self.t_in[next_i] == self.t_out[i]
                - self.steps[next_i]['overlap']
            ).OnlyEnforceIf(self.actives[i])\
                .OnlyEnforceIf(self.actives[next_i])


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
                model.Add(self.t_in[i] < self.t_in[j]) \
                    .OnlyEnforceIf(self.actives[i]) \
                    .OnlyEnforceIf(self.actives[j])


def _add_precedence_constraints(
        self,
        model: cp_model.CpModel
) -> None:
    """Ensure that the precedence between trains is well respected.

    Multiple constraints are created to ensure we can know which steps
    follow directly which other steps.

    This corresponds ton constraints from 8 to 13 in the model
    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """
    # build a map of step per zone
    step_per_zone = {}
    for step in self.steps:
        if not step['zone'] in step_per_zone:
            step_per_zone[step['zone']] = []
        step_per_zone[step['zone']].append(step)

    # Constraints 8a
    for i, step_i in enumerate(self.steps):
        for j, step_j in enumerate(self.steps):
            if (
                step_i["zone"] == step_j["zone"]
                and step_i["train"] != step_j["train"]
            ):
                for ni in step_i["nexts"]:
                    for nj in step_j["nexts"]:
                        if self.steps[ni]["zone"] != self.steps[nj]["zone"]:
                            model.Add(self.diff_itineraries[i][j] == 1)\
                                .OnlyEnforceIf(self.actives[ni])\
                                .OnlyEnforceIf(self.actives[nj])

    # Constraints 8 and 9 from the model
    for steps_of_zone in step_per_zone.values():
        model.AddExactlyOne(self.firsts[step['idx']] for step in steps_of_zone)
        model.AddExactlyOne(self.lasts[step['idx']] for step in steps_of_zone)

    for i, step in enumerate(self.steps):
        all_others_before: Sequence = [self.lasts[i]]
        all_others_after: Sequence = [self.firsts[i]]
        for j, other in enumerate(self.steps):
            if (
                step['train'] != other['train']
                and step['zone'] == other['zone']
            ):
                all_others_before.append(self.precs[i][j])
                all_others_after.append(self.precs[j][i])
                # Constraint 10
                model.AddAtMostOne([self.precs[i][j], self.precs[j][i]])
                # Constraint 11
                model.Add(
                    self.t_out[i]
                    + self.itinierary_setup * self.diff_itineraries[i][j]
                    <= self.t_in[j]) \
                    .OnlyEnforceIf(self.precs[i][j])

        # Constraint 12
        model.Add(
            cp_model.LinearExpr.Sum(all_others_before) == self.actives[i])
        # Constraint 13
        model.Add(
            cp_model.LinearExpr.Sum(all_others_after) == self.actives[i])


def _add_itineraries_constraints(
        self,
        model: cp_model.CpModel
) -> None:
    """Ensure that only one itinerary is taken for each option.
    Also link step activation to their itinierary counter part

    Parameters
    ----------
    model : cp_model.CpModel
        model to fill
    """

    # Constraint A
    for it_option in self.itineraries:
        model.AddExactlyOne(it_option)

    # Constraint B
    for o, option in enumerate(self.options):
        for i, it in enumerate(option.trajectories):
            for s in it.steps:
                model.Add(self.itineraries[o][i] == self.actives[s])
