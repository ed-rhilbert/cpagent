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
    self.arrivals = [
        model.NewIntVar(
            step['min_arrival'],
            step['min_arrival'] if step['prev'] == -1
            else cp_model.INT32_MAX,
            f"arrivals[{i}]")
        for i, step in enumerate(self.steps)]
    self.departures = [
        model.NewIntVar(
            step['min_departure'],
            cp_model.INT32_MAX,
            f"departures[{i}]")
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
            self.arrivals[i],
            self.durations[i],
            self.departures[i],
            f"departures[{i}]")
        for i, step in enumerate(self.steps)]
