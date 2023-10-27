## Constraint Programming Model

version = v1.0.0

### Input data

- $`Nb\_Zones \subset \mathbf{N}`$ : The number of zones
- $`Nb\_Trains \subset \mathbf{N}`$ : The number of trains
- $`Nb\_Steps \subset \mathbf{N}`$ : The number of steps



- $`train_s \in \{1..Nb\_Trains\}, \forall s \in \{1..Nb\_Steps\}`$ : The train associated with the step s
- $`zone_s \in \{1..Nb\_Zones\}, \forall s \in \{1..Nb\_Steps\}`$ : The zone associated with the step s
- $`prev_s \in \{0..Nb\_Steps\}, \forall s \in \{1..Nb\_Steps\}`$ : The step preceding s (0 if None)


- $`min\_arrival_s \in \mathbf{N}, \forall s \in \{1..Nb\_Steps\}`$ : The min arrival time of a step
- $`min\_departure_s \in \mathbf{N}, \forall s \in \{1..Nb\_Steps\}`$ : The min departure time of a step
- $`min\_duration_s \in \mathbf{N}, \forall s \in \{1..Nb\_Steps\}`$ : The min duration of a step

- $`is\_fixed_s \in \{True, False\}, \forall s \in \{1..Nb\_Steps\}`$ : If the duration of a step cannot be changed

### Decision variables

- $`arrival_s \in \mathbf{N}, \forall s \in \{1..Nb\_Steps\}`$ : The arrival time of a step
- $`departure_s \in \mathbf{N}, \forall s \in \{1..Nb\_Steps\}`$ : The departure time of a step

### Constraints

- Two trains shouldn't collide

$`\forall s1, s2 \in \{1..Nb\_Steps\} \; s.t. \; s1 < s2, arrival_{s1} \geq departure_{s2} \lor departure_{s1} \leq arrival_{s2}`$

- A step cannot overtake its reference

$`\forall s \in \{1..Nb\_Steps\}, arrival_s \geq min\_arrival_s`$
$`\forall s \in \{1..Nb\_Steps\}, departure_s \geq min\_departure_s`$

- A step shall last longer than its min duration

$`\forall s \in \{1..Nb\_Steps\}, departure_s - arrival_s \geq min\_duration_s`$

- The duration of a step that is fixed should not be changed

$`\forall s \in \{1..Nb\_Steps\} \; s.t. \; is\_fixed_s = True, departure_s - arrival_s = min\_duration_s`$

- The arrival time at a step is equal to the departure time of the prev step

$`\forall s \in \{1..Nb\_Steps\} \; s.t. \; prev_s \neq 0, arrival_s = departure_{prev_s}`$

- On the first step, arrival must be equal to the reference (min_arrival)

$`\forall s \in \{1..Nb\_Steps\} \; s.t. \; prev_s = 0, arrival_s = min\_arrival_s`$


### Objective

- We minimize the sum of departure delays

$`minimize \sum_{s \in \{1..Nb\_Steps\}} departure_s - min\_departure_s`$