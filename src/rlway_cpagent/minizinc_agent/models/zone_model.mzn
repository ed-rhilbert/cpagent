include "globals.mzn";

% Data

int: N_zones;
int: N_trains;
int: N_steps;

array[1..N_steps] of 1..N_trains: train; % Train associated to a step
array[1..N_steps] of 1..N_zones: zone; % Zone associated to a step
array[1..N_steps] of 0..N_steps: prev; % Previous step

array[1..N_steps] of int: min_arrival; % Min arrival time of a step
array[1..N_steps] of int: min_departure; % Min departure time of a step
array[1..N_steps] of int: min_duration; % Min duration of a step

array[1..N_steps] of bool: is_fixed;

% Variables

array[1..N_steps] of var int: arrival; % Arrival time of a step
array[1..N_steps] of var int: departure; % Departure time of a step

% Constraints

% 1. Two trains shouldn't collide 
constraint forall(z in 1..N_zones)(
  disjunctive(
    [arrival[s] | s in 1..N_steps where zone[s] == z], 
    [departure[s] - arrival[s] | s in 1..N_steps where zone[s] == z])
);

% 2. A step cannot overtake its reference
constraint forall(s in 1..N_steps) (
  arrival[s] >= min_arrival[s] /\
  departure[s] >= min_departure[s]
);

% 3. A step shall last longer than its min duration
constraint forall(s in 1..N_steps) (
  departure[s] - arrival[s] >= min_duration[s]
);

% 4. The duration of a step that is fixed should not be changed
constraint forall(s in 1..N_steps where is_fixed[s])(
  departure[s] - arrival[s] = min_duration[s]
);

% 5. The arrival time at a step is equal to the departure time of the prev step
constraint forall(s in 1..N_steps where prev[s] > 0) (
  arrival[s] = departure[prev[s]]
);

% 6. On the first step, arrival must be equal to the reference (min_arrival)
constraint forall(s in 1..N_steps where prev[s] == 0) (
  arrival[s] = min_arrival[s]
);

% Objectives

% We minimize the sum of departure delays
solve minimize sum(s in 1..N_steps)(departure[s] - min_departure[s]);