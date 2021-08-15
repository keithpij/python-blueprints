import argparse
import os
import time

import ray


SLEEP_TIME = 2


@ray.remote
def long_running_task(x):
    time.sleep(SLEEP_TIME) # Replace this is with work you need to do.
    return x


@ray.remote
def fibonacci_distributed(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size


def fibonacci_local(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size


def run_remote(sequence_size):
    ray.init()
    start_time = time.time()
    results = ray.get([fibonacci_distributed.remote(sequence_size) for x in range(os.cpu_count())])
    duration = time.time() - start_time
    print('Sequence size: {}, Remote execution time: {}'.format(sequence_size, duration))


def run_local(sequence_size):
    start_time = time.time()
    results = [fibonacci_local(sequence_size) for _ in range(os.cpu_count())]
    duration = time.time() - start_time
    print('Sequence size: {}, Local execution time: {}'.format(sequence_size, duration))


if __name__ == '__main__':

    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--remote',
                        help='Run the tasks remotely (parallel).',
                        action='store_true')
    parser.add_argument('-l', '--local',
                        help='Run the tasks locally (sequential).',
                        action='store_true')
    parser.add_argument('-b', '--both',
                        help='Run both local and remote tasks.',
                        action='store_true')
    parser.add_argument('-s', '--size',
                        help='Sequence size.')
    parser.add_argument('-d', '--dashboard',
                        help='Start dashboard.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message if something is wrong.
    args = parser.parse_args()
    if args.size:
        sequence_size = int(args.size)
    else:
        sequence_size = 10000

    if args.local:
        run_local(sequence_size)

    if args.remote:
        run_remote(sequence_size)

    if args.both:
        run_local(sequence_size)
        run_remote(sequence_size)

    if args.dashboard:
        ray.init(num_cpus=2)
        input('Press <return> to close the Ray dashboard. --> ')
