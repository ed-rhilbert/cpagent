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
            step['min_t_in'] if step['prev'] == -1
            else cp_model.INT32_MAX,
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
