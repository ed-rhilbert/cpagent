include "globals.mzn";

% Données

int: Z; %Le nombre de zones
int: T; %Le nombre de trains
int: S; %Le nombre d'étapes (train passant par une zone)

array[1..S] of 1..T: train; %Le train associé à une étape
array[1..S] of 1..Z: zone; %La zone associée à une étape
array[1..S] of 0..S: prev; %L'étape précédente

array[1..S] of int: min_arrival; %L'heure d'arrivée min d'une étape
array[1..S] of int: min_departure; %L'heure de départ min d'une étape
array[1..S] of int: min_duration; %La durée min d'une étape

array[1..S] of bool: is_fixed;

% Variables

array[1..S] of var int: a; %heure d'arrivée d'une étape
array[1..S] of var int: d; %heure de départ d'une étape

% Contraintes

%Pas de collisions
constraint forall(z in 1..Z)(
  disjunctive(
    [a[s] | s in 1..S where zone[s] == z], 
    [d[s] - a[s] | s in 1..S where zone[s] == z])
);

%On ne peut pas dépasser la référence
constraint forall(s in 1..S) (
  a[s] >= min_arrival[s] /\
  d[s] >= min_departure[s]
);

%Le train doit passer plus de temps dans une zone que la durée min
constraint forall(s in 1..S) (
  d[s] - a[s] >= min_duration[s]
);

%Certaines étapes ont une durée fixe
constraint forall(s in 1..S where is_fixed[s])(
  d[s] - a[s] = min_duration[s]
);

%Succession des étapes
constraint forall(s in 1..S where prev[s] > 0) (
  a[s] = d[prev[s]]
);

%Contrainte sur la première étape
constraint forall(s in 1..S where prev[s] == 0) (
  a[s] = min_arrival[s]
);

%Fonction objectif
solve minimize sum(s in 1..S)(d[s] - min_departure[s]);