"""
Flexible CPU load generator.
"""
from contextlib import contextmanager
from enum import Enum
import logging
import multiprocessing as mp
from queue import Empty, Queue
from os import cpu_count
import random
import time
from typing import Any, Final, Iterator, cast

import click
import psutil


class _P(float):
    """
    The class that represents percentage.
    """

    def clamp(self) -> "_P":
        """
        Clamp the percentage between 0 and 100.
        """
        return _P(min(max(self, 0.0), 100.0))


class _CM(Enum):
    """
    Possible control messages for workers.
    """

    start = "start"
    stop = "stop"


_M = _P | _CM


def _molotilka(num: int, q: Queue[_M]) -> None:
    def dbg(*args: Any) -> None:
        logging.debug(f"Worker {num}: {args[0]}", *args[1:])

    dbg("Created.")

    # Wait for start message
    m = q.get(block=True)
    dbg(f"Got message '{m}'.")
    if m != _CM.start:
        raise RuntimeError("Process was not started, cannot accept commands.")
    m = q.get(block=True)
    dbg(f"Got message '{m}'.")
    while True:
        if isinstance(m, _CM):
            if m == _CM.start:
                raise RuntimeError("The process was already started.")
            elif m == _CM.stop:
                # Actually, never should happen.
                dbg("Graceful exit.")
                break
            raise RuntimeError(f"Unknown control message {m}.")
        # Now m is the desired load percentage.
        if m > 0.0:
            start = time.monotonic()
            useless = [random.betavariate(0.2, 0.4) for _ in range(10000)]
            useless.sort()
            elapsed = time.monotonic() - start
            # We suppose here that useless work takes all CPU and sleep
            # taxes none.
            time.sleep(elapsed * (100.0 - m) / m)
            try:
                # Check if we got new load valuo
                m = q.get(block=False)
                dbg(f"Got message '{m}'.")
            except Empty:
                # If we did not, continue with what we have
                pass
        else:
            # Load was zero, wait for new load
            dbg("Waiting for the next message.")
            m = q.get(block=True)
            dbg(f"Got message '{m}'.")


def _turn_on_debug(
    _ctx: click.Context,  # pyright: ignore
    _param: click.Parameter,  # pyright: ignore
    debug: bool,
) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


@contextmanager
def _spawn_workers() -> Iterator[list[Queue[_P]]]:
    cpus = cpu_count()
    if cpus is None:
        yield []
        return

    logging.debug(f"Creating {cpus} workers.")
    queues: list[Queue[_M]] = [mp.Queue(maxsize=1) for _ in range(cpus)]
    workers = [
        mp.Process(target=_molotilka, args=(num, q))
        for num, q in enumerate(queues)
    ]
    for w in workers:
        w.start()
    for q in queues:
        logging.debug("Sending start message to worker.")
        logging.debug(q)
        q.put(_CM.start, block=True)
    yield cast(list[Queue[_P]], queues)

    for q in queues:
        logging.debug("Sending stop message to worker.")
        q.put(_CM.stop, block=True)
    for w in workers:
        w.terminate()


@click.command()
@click.argument(
    "load",
    type=click.FloatRange(0.0, 100.0, min_open=True),
)
@click.option(
    "-d",
    "--stddev",
    type=click.FloatRange(0.0, 100.0),
    default=0.0,
    help="Standard deviation for system load (in percents). Default is 0.",
)
@click.option(
    "-s",
    "--step",
    type=click.FloatRange(0.0, 100.0, min_open=True, max_open=True),
    default=4.5,
    help="Adjust system load by steps, given by this number (in percents)."
    "Default is 4.5.",
)
@click.option(
    "-e",
    "--epsilon",
    type=click.FloatRange(0.0, 100.0, min_open=True),
    default=1.0,
    help="If system load is within this number (in percents) of the target, "
    "do not adjust. Default is 1.0.",
)
@click.option(
    "-t",
    "--time-period",
    type=click.FloatRange(0.0, min_open=True),
    default=3.7,
    help="Do not change system load during the given time (in seconds). "
    "Default is 3.7.",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    expose_value=False,
    callback=_turn_on_debug,
    help="Debug logging.",
)
def main(
    load: float, stddev: float, step: float, epsilon: float, time_period: float
) -> None:
    """
    Create given CPU load with the given standard devialtion.
    """
    step_p: Final[_P] = _P(step)
    epsilon_p: Final[_P] = _P(epsilon)

    with _spawn_workers() as queues:
        if not queues:
            raise RuntimeError(
                "Cannot determine the number of CPUs in the system."
            )
        work_p = _P(0.0)
        while True:
            logging.debug("Sleeping for %s seconds.", time_period)
            time.sleep(time_period)
            current_p = _P(psutil.cpu_percent())
            logging.debug("Current CPU load is %s%%", round(current_p, 2))
            willing_p = _P(load + random.normalvariate(0.0, stddev)).clamp()
            logging.debug("Willing to get %s%%", round(willing_p, 2))
            if willing_p - epsilon_p <= current_p <= willing_p + epsilon_p:
                logging.debug("System load is good, doing nothing.")
                continue
            elif current_p > willing_p + epsilon_p:
                logging.debug("System load is too high.")
                change_p = _P(min(step_p, current_p - willing_p))
                work_p = _P(work_p - change_p).clamp()
            else:
                logging.debug("System load is too low.")
                change_p = _P(min(step_p, -current_p + willing_p))
                work_p = _P(work_p + change_p).clamp()
            logging.debug(
                "Asking workers to generate %s%% load", round(work_p, 2)
            )
            for q in queues:
                q.put(work_p, block=True)


if __name__ == "__main__":
    main()
