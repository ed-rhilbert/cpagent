## Constraint Programming Model

version = v1.0.0

### Input data

- $N_{zones} \in \mathbb{N}$ : The number of zones
- $N_{trains} \in \mathbb{N}$ : The number of trains
- $N_{steps} \in \mathbb{N}$ : The number of steps



- $train_s \in \{1..N_{trains}\}, \forall s \in \{1..N_{steps}\}$ : The train associated with the step s
- $zone_s \in \{1..N_{zones}\}, \forall s \in \{1..N_{steps}\}$ : The zone associated with the step s
- $prev_s \in \{0..N_{steps}\}, \forall s \in \{1..N_{steps}\}$ : The step preceding s (0 if None)


- $min\_arrival_s \in \mathbb{N}, \forall s \in \{1..N_{steps}\}$ : The min arrival time of a step
- $min\_departure_s \in \mathbb{N}, \forall s \in \{1..N_{steps}\}$ : The min departure time of a step
- $min\_duration_s \in \mathbb{N}, \forall s \in \{1..N_{steps}\}$ : The min duration of a step

- $is\_fixed_s \in \{True, False\}, \forall s \in \{1..N_{steps}\}$ : If the duration of a step cannot be changed

### Decision variables

- $arrival_s \in \mathbb{N}, \forall s \in \{1..N_{steps}\}$ : The arrival time of a step
- $departure_s \in \mathbb{N}, \forall s \in \{1..N_{steps}\}$ : The departure time of a step

### Constraints

- Two trains shouldn't collide

$\forall s1, s2 \in \{1..N_{steps}\} \; s.t. \; s1 < s2, arrival_{s1} \geq departure_{s2} \lor departure_{s1} \leq arrival_{s2}$

- A step cannot overtake its reference

$\forall s \in \{1..N_{steps}\}, arrival_s \geq min\_arrival_s$
$\forall s \in \{1..N_{steps}\}, departure_s \geq min\_departure_s$

- A step shall last longer than its min duration

$\forall s \in \{1..N_{steps}\}, departure_s - arrival_s \geq min\_duration_s$

- The duration of a step that is fixed should not be changed

$\forall s \in \{1..N_{steps}\} \; s.t. \; is\_fixed_s = True, departure_s - arrival_s = min\_duration_s$

- The arrival time at a step is equal to the departure time of the prev step

$\forall s \in \{1..N_{steps}\} \; s.t. \; prev_s \neq 0, arrival_s = departure_{prev_s}$

- On the first step, arrival must be equal to the reference (min_arrival)

$\forall s \in \{1..N_{steps}\} \; s.t. \; prev_s = 0, arrival_s = min\_arrival_s$


### Objective

- We minimize the sum of departure delays

$minimize \sum_{s \in \{1..N_{steps}\}} departure_s - min\_departure_s$