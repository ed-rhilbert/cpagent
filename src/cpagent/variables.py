from ortools.sat.python import cp_model


def _create_variables(
        self,
        model: cp_model.CpModel) -> None:
    """Create the set of decision variables

    Parameters
    ----------
    model : cp_model.CpModel
        The model to fill
    """
    self.t_in = [
        model.NewIntVar(
            step['min_t_in'],
            cp_model.INT32_MAX,
            f"t_in[{i}]")
        for i, step in enumerate(self.steps)]
    self.t_out = [
        model.NewIntVar(
            step['min_t_out'],
            cp_model.INT32_MAX,
            f"t_out[{i}]")
        for i, step in enumerate(self.steps)]
    self.durations = [
        model.NewIntVar(
            step['min_duration'],
            step['min_duration'] if step['is_fixed']
            else cp_model.INT32_MAX,
            f"durations[{i}]")
        for i, step in enumerate(self.steps)]
    self.intervals = [
        model.NewIntervalVar(
            self.t_in[i],
            self.durations[i],
            self.t_out[i],
            f"t_out[{i}]")
        for i, step in enumerate(self.steps)]

    # Precedence variables

    # first_si : 1 if the step si is the first step to pass in its zone
    # last_si : 1 if the step si is the last step to pass in its zone
    # prec_si_sj : 1 if the step si is just before the step sj
    #               for this to be true the two steps needs to be the same zone
    #               and different trains
    # diff_itinerary_si_sj : 1 if the step si and sj have a different zone
    #                        AFTER the one they share

    self.firsts = [
        model.NewIntVar(
            0,
            1,
            f"first_s{i}")
        for i, _ in enumerate(self.steps)]
    self.lasts = [
        model.NewIntVar(
            0,
            1,
            f"last_s{i}")
        for i, _ in enumerate(self.steps)]
    self.precs = [
        [
            model.NewIntVar(
                0,
                1 if (
                    step_i["train"] != step_j["train"]
                    and step_i["zone"] == step_j["zone"]
                )
                else 0,
                f"prec_s{i}_s{j}")
            for i, step_i in enumerate(self.steps)
        ]
        for j, step_j in enumerate(self.steps)
    ]

    self.diff_itineraries = [
        [
            model.NewIntVar(
                1 if (
                    step_i["next"] >= 0
                    and step_j["next"] >= 0
                    and (
                        self.steps[step_i["next"]]["zone"]
                        != self.steps[step_j["next"]]["zone"]
                    )
                )
                else 0,
                1,
                f"diff_itinierary_s{i}_s{j}")
            for i, step_i in enumerate(self.steps)
        ]
        for j, step_j in enumerate(self.steps)
    ]
