# Constraint Programming Model

version = v1.1.0

## Description

Zones are physically defined portions of the intrastructure, delimited by two detectors, or a detector and a buffer stop. Zones can be :
- a station lane (where the trains can stop),
- a block beween two stations (in which the trains can accelerate/decelerate),
- a switch, or a set of switches (in which the trains can not stop).

A train trajectory is composed of a succession of **steps**, each step being defined by:
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

**Arrival and departure times**
- $min\_arrival_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The min arrival time of a step
- $min\_departure_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The min departure time of a step
- $min\_duration_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The min duration of a step

**Constraint depending on the type of zone (lane, block, switch...)**
- $is\_fixed_s \in \{True, False\}, \forall s \in \{1,..,N_{steps}\}$ : If the duration of a step cannot be changed

## Decision variables

- $arrival_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The arrival time of a step
- $departure_s \in \mathbb{N}, \forall s \in \{1,..,N_{steps}\}$ : The departure time of a step

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

7. _OPTIONAL_ A train cannot overtake another train (we use the reference ($min\_arrival$) to determine the order of trains)

$$\forall s1, s2 \in \{1,...,N_{steps}\}\;s.t.\;  min\_arrival_{s1} < min\_arrival_{s2},\\
arrival_{s1} < arrival_{s2}$$
