import argparse
import logging
import os
import threading
import time

from numpy import random
import ray


@ray.remote
def distributed_task(param: int):
    time.sleep(random.uniform(0, 4))
    return param


def process_all(results):
    total = 0
    for x in results:
        time.sleep(1)
        total += x
    return total


def process_incremental(total, result):
    time.sleep(1)
    return total + result


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pipeline',
                        help='Pipeline tasks, process as they complete.',
                        action='store_true')

    parser.add_argument('-w', '--wait',
                        help='Wait for all tasks to complete.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message if something is wrong.
    args = parser.parse_args()

    if args.wait:
        ray.init()
        START_TIME = time.time()
        DATA_LIST = ray.get([distributed_task.remote(x) for x in range(4)])
        SUM = process_all(DATA_LIST)
        DELTA = time.time() - START_TIME
        print('Wait execution time: {}'.format(DELTA))
        print('Sum: {}'.format(SUM))
        input('Press <return> to close the Ray dashboard. --> ')

    if args.pipeline:
        ray.init()
        START_TIME = time.time()
        FUTURES = [distributed_task.remote(x) for x in range(4)]
        SUM = 0
        while len(FUTURES):
            done_id, FUTURES = ray.wait(FUTURES)
            SUM = process_incremental(SUM, ray.get(done_id[0]))
        DELTA = time.time() - START_TIME
        print('Pipeline execution time: {}'.format(DELTA))
        print('Sum: {}'.format(SUM))
        input('Press <return> to close the Ray dashboard. --> ')
