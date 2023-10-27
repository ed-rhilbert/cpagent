include "globals.mzn";

% Data

int: Nb_Zones;
int: Nb_Trains;
int: Nb_Steps;

array[1..Nb_Steps] of 1..Nb_Trains: train; % Train associated to a step
array[1..Nb_Steps] of 1..Nb_Zones: zone; % Zone associated to a step
array[1..Nb_Steps] of 0..Nb_Steps: prev; % Previous step

array[1..Nb_Steps] of int: min_arrival; % Min arrival time of a step
array[1..Nb_Steps] of int: min_departure; % Min departure time of a step
array[1..Nb_Steps] of int: min_duration; % Min duration of a step

array[1..Nb_Steps] of bool: is_fixed;

% Variables

array[1..Nb_Steps] of var int: arrival; % Arrival time of a step
array[1..Nb_Steps] of var int: departure; % Departure time of a step

% Constraints

% No Collisions
constraint forall(z in 1..Nb_Zones)(
  disjunctive(
    [arrival[s] | s in 1..Nb_Steps where zone[s] == z], 
    [departure[s] - arrival[s] | s in 1..Nb_Steps where zone[s] == z])
);

% A step cannot overtake its reference
constraint forall(s in 1..Nb_Steps) (
  arrival[s] >= min_arrival[s] /\
  departure[s] >= min_departure[s]
);

% A step shall last longer than its min duration
constraint forall(s in 1..Nb_Steps) (
  departure[s] - arrival[s] >= min_duration[s]
);

% The duration of a step that is fixed should not be changed
constraint forall(s in 1..Nb_Steps where is_fixed[s])(
  departure[s] - arrival[s] = min_duration[s]
);

% The arrival time at a step is equal to the departure time of the prev step
constraint forall(s in 1..Nb_Steps where prev[s] > 0) (
  arrival[s] = departure[prev[s]]
);

% On the first step, arrival must be equal to the reference (min_arrival)
constraint forall(s in 1..Nb_Steps where prev[s] == 0) (
  arrival[s] = min_arrival[s]
);

% Objectives

% We minimize the sum of departure delays
solve minimize sum(s in 1..Nb_Steps)(departure[s] - min_departure[s]);