import argparse
import logging
import os
import threading

from numpy import random
import ray
import time


LENGTH_THRESHOLD = 200000


def print_system_info():
    print('OS Name:  {}'.format(os.name))
    print('CPUs:  {}'.format(os.cpu_count()))
    print('Process ID:  {}'.format(os.getpid()))
    print('Thread ID:  {}'.format(threading.get_ident()))


def partition(collection):
    """
    This function will break the passed in collection into two collections based on the
    value of the last element.
    """
    pivot = collection.pop()
    greater, lesser = [], []
    for element in collection:
        if element > pivot:
            greater.append(element)
        else:
            lesser.append(element)
    return lesser, pivot, greater


@ray.remote
def quick_sort_distributed(collection):
    print('Process ID:  {}'.format(os.getpid()))
    if len(collection) <= LENGTH_THRESHOLD:
        return sorted(collection)
    else:
        lesser, pivot, greater = partition(collection)
        lesser = quick_sort_distributed.remote(lesser)
        greater = quick_sort_distributed.remote(greater)
        return ray.get(lesser) + [pivot] + ray.get(greater)


def quick_sort(collection):
    if len(collection) <= LENGTH_THRESHOLD:
        return sorted(collection)
    else:
        lesser, pivot, greater = partition(collection)
        lesser = quick_sort(lesser)
        greater = quick_sort(greater)
        return lesser + [pivot] + greater


def create_sample_data():
    unsorted = random.randint(100000, size=4000000).tolist()
    return unsorted


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dashboard',
                        help='Start dashboard.',
                        action='store_true')
    parser.add_argument('-s', '--sort',
                        help='Run the sort demo.',
                        action='store_true')
    parser.add_argument('-sys', '--system',
                        help='Print system information.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message if something is wrong.
    args = parser.parse_args()

    if args.system:
        print_system_info()

    if args.dashboard:
        ray.init()
        input('Press <return> to close the Ray dashboard. --> ')

    if args.sort:
        logging.getLogger().setLevel(logging.ERROR)
        ray.init()
        UNSORTED = create_sample_data()
        START_TIME = time.time()
        quick_sort(UNSORTED)
        DELTA = time.time() - START_TIME
        print('Non-distrubuted execution time: {}'.format(DELTA))

        START_TIME = time.time()
        ray.get(quick_sort_distributed.remote(UNSORTED))
        DELTA = time.time() - START_TIME
        print('Distrubuted execution time: {}'.format(DELTA))
        input('Press <return> to close the Ray dashboard. --> ')
