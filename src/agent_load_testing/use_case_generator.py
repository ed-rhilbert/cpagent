import itertools
import random
import numpy as np

from rlway.schedules import Schedule

from rlway_cpagent.osrd_adapter import regulation_problem_from_schedule
from rlway_cpagent.regulation_solver import CpRegulationProblem


TRAIN_SPWAN_INTERVAL = 10
STEP_DURATION = 10
TRAIN_DELAY = 5

NB_CONNECTING_TRACKS = 2
NB_PLATFORM = 2

GEOMETRIC_PROBA = 0.2


def generate_use_case(
        nb_stations: int,
        nb_trains: int) -> CpRegulationProblem:
    """Generate a rlway use case in a Schedule format

    A station is defined by NB_PLATFORM parallel tracks links to
    NB_CONNECTING_TRACKS consecutive tracks.
    Exemple NB_PLATFORM = 2, NB_CONNECTING_TRACKS = 2 :
        _T1_
      /      \
               --T3----T4--
      \ _T2_ /

    If nb_stations > 1, the stations are linked :

        _T1_                  _T5_
      /      \              /      \
               --T3----T4--          --T7----T8--
      \ _T2_ /              \ _T6_ /

    Trains are circulating forward on the infrastructure.
    At each station, a train with the type i circulate on the i_th platform
    modulo the number of plateform in the station.

    Parameters
    ----------
    nb_stations : int
        number of stations
    nb_trains : int
        number of trains

    Returns
    -------
    Schedule
        Generated Schedule
    """
    nb_tracks_in_station = NB_PLATFORM + NB_CONNECTING_TRACKS
    nb_zones = nb_stations * nb_tracks_in_station
    ref_schedule = Schedule(nb_zones, nb_trains)
    delayed_schedule = Schedule(nb_zones, nb_trains)

    delay = TRAIN_DELAY
    for train_idx in range(nb_trains):
        path = list(itertools.chain.from_iterable(
            [
                [station_idx*nb_tracks_in_station + train_idx % NB_PLATFORM]
                + [
                    station_idx*nb_tracks_in_station + NB_PLATFORM + i
                    for i in range(NB_CONNECTING_TRACKS)
                ]
                for station_idx in range(nb_stations)
            ]
        ))

        ref_start = train_idx * TRAIN_SPWAN_INTERVAL
        delayed_start = train_idx * TRAIN_SPWAN_INTERVAL

        for zone_idx in path:
            ref_schedule.set(
                train_idx,
                zone_idx,
                (ref_start, ref_start + STEP_DURATION))
            delayed_schedule.set(
                train_idx,
                zone_idx,
                (delayed_start, delayed_start + STEP_DURATION + delay))
            ref_start = ref_start + STEP_DURATION
            delayed_start = delayed_start + STEP_DURATION + delay
            delay = 0

    return regulation_problem_from_schedule(ref_schedule, delayed_schedule,
                                            None, None)


def generate_garage_use_case(
        nb_stations: int,
        nb_trains: int,
        delay_proba: float = 0.2) -> CpRegulationProblem:
    nb_tracks_in_station = NB_PLATFORM + NB_CONNECTING_TRACKS
    nb_zones = nb_stations * nb_tracks_in_station + nb_trains + 1
    nb_tracks_in_garage = nb_trains + 1
    ref_schedule = Schedule(nb_zones, nb_trains)
    delayed_schedule = Schedule(nb_zones, nb_trains)

    for train_idx in range(nb_trains):
        path = [train_idx, nb_trains]
        path += list(itertools.chain.from_iterable(
            [
                [station_idx*nb_tracks_in_station + train_idx % NB_PLATFORM
                 + nb_tracks_in_garage]
                + [
                    station_idx*nb_tracks_in_station + NB_PLATFORM + i
                    + nb_tracks_in_garage
                    for i in range(NB_CONNECTING_TRACKS)
                ]
                for station_idx in range(nb_stations)
            ]
        ))

        ref_start = train_idx * TRAIN_SPWAN_INTERVAL
        delayed_start = train_idx * TRAIN_SPWAN_INTERVAL

        for zone_idx in path:
            ref_schedule.set(
                train_idx,
                zone_idx,
                (ref_start, ref_start + STEP_DURATION))
            zone_delay = np.random.geometric(GEOMETRIC_PROBA) \
                if random.random() < delay_proba else 0
            delayed_schedule.set(
                train_idx,
                zone_idx,
                (delayed_start, delayed_start + STEP_DURATION + zone_delay))
            ref_start = ref_start + STEP_DURATION
            delayed_start = delayed_start + STEP_DURATION + zone_delay

    return regulation_problem_from_schedule(ref_schedule, delayed_schedule,
                                            None, None)
