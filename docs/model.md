# Constraint Programming Model

version = v1.1.0

## Description

Zones are physically defined portions of the intrastructure, delimited by two detectors, or a detector and a buffer stop. Zones can be :
- a station lane (where the trains can stop),
- a block beween two stations (in which the trains can accelerate/decelerate),
- a switch, or a set of switches (in which the trains can not stop).

A train path is composed of a succession of **steps**, each step being defined by:
  - a zone
  - a train
  - its arrival and departure times in the zone, in seconds

Given an original valid timetable and a delay, the goal of the model is to find the best values for the times at which trains enter/leave the zones, that minimize the total induced delay, under the constraints that
- the trains follow their trajectories, i.e. a given succession of steps,
  - A train can be in multiple zones at the same time (for example its head can be in a zone while its tail is in another zone). The time between the entry of a train in a zone and the exit from the precedent zone is computed based on the valid timetable.
- two trains can not be in the same zone at the same time,
- the trains can not go faster than a reference given by a standalone base simulation,
- trains can stop at stations, decelerate in blocks between stations,
- trains can not stop or decelerate on switches.
- OPTIONAL : trains cannot overtake

## Input data

The following data are retrieved from the results of an OSRD simulation.

**Sizes**
- $N_{zones} \in \mathbb{N}$ : The number of zones
- $N_{trains} \in \mathbb{N}$ : The number of trains
- $N_{steps} \in \mathbb{N}$ : The number of steps

**Steps definitions and ordering**
- $train_s \in \{1,..,N_{trains}\}, \forall s \in \{1,..,N_{steps}\}$ : The train associated with the step $s$
- $zone_s \in \{1,..,N_{zones}\}, \forall s \in \{1,..,N_{steps}\}$ : The zone associated with the step $s$
- $prev_s \in \{0..N_{steps}\}, \forall s \in \{1,..,N_{steps}\}$ : The step preceding $s$ (0 if None)
- $next_s \in \{0..N_{steps}\}, \forall s \in \{1,..,N_{steps}\}$ : The step following $s$ (0 if None)

**Arrival and departure times**
- $min\_arrival_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The min arrival time of a step
- $min\_departure_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The min departure time of a step
- $min\_duration_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The min duration of a step

**Constraint depending on the type of zone (lane, block, switch...)**
- $is\_fixed_s \in \{True, False\}, \forall s \in \{1,..,N_{steps}\}$ : If the duration of a step cannot be changed

**Constants**
- $T_c$ : The time setup to change between to different itineraries

## Decision variables

- $arrival_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The arrival time of a step
- $departure_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The departure time of a step

## Intermediate variables

- $prec_i^j \in \{0, 1\}, \forall i \in \{1,..,N_{steps}\}, \forall j \in \{1,..,N_{steps}\}$ : $1$ if step $j$ directly follows step $i$ on $zone_i$. It follows the basic structural constraint :
$$
zone_i \ne zone_j \text{ or } train_j = train_i \implies prec_i^j = 0
$$
- $first_s \in \{0, 1\}, \forall s \in \{1,..,N_{steps}\}$ : $1$ if the step is the first on $zone_s$.
- $last_s \in \{0, 1\}, \forall s \in \{1,..,N_{steps}\}$ : $1$ if the step is the last on $zone_s$.
- $diff\_it_i ^j \in \{0, 1\}, \forall i \in \{1,..,N_{steps}\}, \forall j \in \{1,..,N_{steps}\}$ : $1$ if and only if the steps $i$ and $j$ are followed by seps with different zone. This can be expressed like this :
$$
diff\_it_i^j = 1 \Leftrightarrow zone_{next_i} \ne zone_{next_j}
$$

## Objective

We minimize the sum of arrival delays

$$\text{minimize}
\sum_{s \in\\{1,..,N_{steps}\\}}^{}\left(
arrival_s - min\_arrival_s
\right)
$$

## Constraints

1. Two trains shouldn't collide

$$\forall s_1, s_2 \in \{1,..,N_{steps}\} \; s.t. \; zone_{s_1} = zone_{s_2}, \\
arrival_{s_1} \geq departure_{s_2} \lor departure_{s_1} \leq arrival_{s_2}$$

2. A step cannot overtake its reference

$$
\left\{
\begin{array}{ll}
\forall s \in \{1,..,N_{steps}\}, &  arrival_s \geq min\_arrival_s\\
\forall s \in \{1,..,N_{steps}\}, & departure_s \geq min\_departure_s\\
\end{array}
\right.
$$

3. A step shall last longer than its min duration

$$\forall s \in \{1,..,N_{steps}\}, departure_s - arrival_s \geq min\_duration_s$$

4. The duration of a step that is fixed should not be changed

$$\forall s \in \{1,..,N_{steps}\} \; s.t. \; is\_fixed_s = True, \\departure_s - arrival_s = min\_duration_s$$

5. The arrival time at a step is equal to the departure time of the prev step minus the overlap computed from the valid timetable.

$$\forall s \in \{1,..,N_{steps}\} \; s.t. \; prev_s \neq 0, \\arrival_s = departure_{prev_s} - overlap_ s$$

6. On the first step, arrival must be equal to the reference ($min\_arrival$)

$$\forall s \in \{1,..,N_{steps}\} \; s.t. \; prev_s = 0, arrival_s = min\_arrival_s$$

### Enforce order (optional)

7. A train cannot overtake another train (we use the reference ($min\_arrival$) to determine the order of trains)

$$\forall s1, s2 \in \{1,...,N_{steps}\}\;s.t.\;  min\_arrival_{s1} < min\_arrival_{s2},\\
arrival_{s1} < arrival_{s2}$$

### Precedence constraints

8. There can only be one step being the first in a zone
$$
\forall z \in N_{zones}\; \sum_{s \in \{zone_s = z\}}first_s=1
$$

9. There can only be one step being the last in a zone
$$
\forall z \in N_{zones}\; \sum_{s \in \{zone_s = z\}}last_s=1
$$

10. If a step $i$ follows a step $j$ then the revese cannot be true
$$
prec_i^j + prec_j^i \le 1
$$

11. For every step $i$ the following step $j$ must starts after the end of step $j$. An itinerary setup is added if the
itineraries are different on the next steps of each $i$ and $j$.

$$
\forall i \in {1,..., N_{steps}}\;\forall j \in {1,..., N_{steps}}\;\\prec_i^j \implies departure_{i} + T_c \times diff\_it_i ^j \le arrival_{j}
$$

12. For every step there must be exactly one following step except if it's the last step on its zone
$$
\forall i \in {1,..., N_{steps}}\;\sum_{j\in \{j, zone_j = zone_i\}} prec_i^j + last_i = 1
$$

13. For every step there must be exactly one previous step except if it's the first step on its zone
$$
\forall i \in {1,..., N_{steps}}\;\sum_{j\in \{j, zone_j = zone_i\}} prec_j^i + first_i = 1
$$

# Model adaptation to allow change of itinerary

This approach would requires alternative paths known in advance for trains.
For example we would know that a train could take on path or another one between two steps.

## Input Data

New data would be required to allow change of itinerary :

**Sizes**
- $N_o \in \mathbb{N}$ : The number of itinerary options
- $N_{itineraries}^o \in \mathbb{N}$ : The number of itinieraries of the option o
- $N_{steps}^i \in \mathbb{N}$ : The number of steps of an itinerary

**Itinerary**
- $S^i \subset \mathbb{N}$ : All steps in the itinerary $i$
- $I^o \subset \mathbb{N}$ : all the itineraries in the option $o$

## Variables

- $i^i \in \{0,1\}$ : boolean that tells us if the itinerary is taken or not
- $active_s \in \{0,1\}$ : boolean that tells us if the step is activated (part of a selected itinerary).

## Constraits

A lot of constraints are modified from the original ones. New constraints are indexed by letters while modified one use the same numbering than previously.

An effort must be taken to give every information even for alternative itineraries.

### New constraints
A. One itinerary must be taken for each options
$$\forall o \in {1,...,N_o}\; \sum_{i\in I^o} i^i = 1
$$

B. A step is active if and only if the itinerary it belongs to is selected.

$$\forall o \in {1,...,N_o}\; \forall i\in I^o, \forall s \in S^i \;\\
active_s = i^i
$$

### Modified constraints

1. Two trains shouldn't collide

$$\forall s_1, s_2 \in \{1,..,N_{steps}\} \; s.t. \; arrival_{s_1} < arrival_{s_1}\; s.t. \; active_{s_1} = active_{s_1} = 1, \\
arrival_{s_1} \geq departure_{s_2} \lor departure_{s_1} \leq arrival_{s_2}$$

5. The arrival time at a step is equal to the departure time of the prev step minus the overlap computed from the valid timetable.

$$\forall s \in \{1,..,N_{steps}\} \; s.t. \; prev_s \neq 0, \\active_{prev_s} \implies arrival_s = departure_{prev_s} - overlap_ s$$

7. _OPTIONAL_ A train cannot overtake another train (we use the reference ($min\_arrival$) to determine the order of trains)

$$\forall s1, s2 \in \{1,...,N_{steps}\}\;\\
s.t.\;  min\_arrival_{s1} < min\_arrival_{s2}\; \\
s.t. \; active_{s_1} = active_{s_1} = 1,\\
arrival_{s1} < arrival_{s2}$$

**Precedence constraint**

No precedence variable can be used if the step is not active.

12. For every step there must be exactly one following step except if it's the last step on its zone
$$
\forall i \in {1,..., N_{steps}}\;\sum_{j\in \{j, zone_j = zone_i\}} prec_i^j + last_i = active_i
$$

13. For every step there must be exactly one previous step except if it's the first step on its zone
$$
\forall i \in {1,..., N_{steps}}\;\sum_{j\in \{j, zone_j = zone_i\}} prec_j^i + first_i = active_i
$$

## Objective

To handle different itineraries it will be required to update the objective function to only account for active steps.

$$\text{minimize}
\sum_{s \in\\{1,..,N_{steps}\\}}^{}\left(
arrival_s - min\_arrival_s
\right)\times active_s
$$
