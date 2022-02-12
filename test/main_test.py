import argparse

from test.utils import *
from structures.sw import SW_n_of_N
from structures.gk import GK
from structures.np_quantile import NumpyQuantile
from test.data_generator import Generator
from test.metric_monitor import Monitor

import json

def main(args):

    epsilon = args.epsilon
    N = args.number_of_points

    algos = {
        'Numpy': NumpyQuantile(
            n=N//10
        ),
        'GK': GK(epsilon=epsilon),
        'SW n-of-N': SW_n_of_N(
            n=N//10,
            epsilon=epsilon
        )
    }

    data_generator = Generator()
    monitor = Monitor(
        algorithms=algos,
        data_generator=data_generator,
        N=N,
        n=N//10
    )

    print('Starting simulation...')
    monitor.run_simulation()

    report = monitor.generate_report()
    with open('report.json', 'w') as f:
        json.dump(report, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Run tests with visualization"
    )

    parser.add_argument(
        '-e',
        '--epsilon',
        type=epsilon_validator,
        default=DEFAULT_EPSILON_PARAMETER,
        help=f'Parameter epsilon for algorthims'
    )

    parser.add_argument(
        '-N',
        '--number-of-points',
        type=number_of_points_validator,
        default=DEFAULT_NUMBER_OF_POINTS,
        help='Number of points to simulate'
    )

    args = parser.parse_args()

    main(args)