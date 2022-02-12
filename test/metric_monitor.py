from test.data_generator import Generator
from typing import List, Dict, Any
import cv2
import numpy as np
from test.utils import id2key
import sys
import time
from tabulate import tabulate

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


class Monitor():
    def __init__(
        self,
        algorithms: Dict[str, Any],
        data_generator: Generator,
        N: int,
        n: int,
        plot_limit: int = 40
    ):
        self.generator = data_generator
        self.algos = algorithms
        self.plot_limit = plot_limit
        assert n < N, f'n can only be less than N. Got n = {n}, N = {N}'
        self.N = N
        self.n = n
        self.memory = {a_name: [] for a_name in algorithms.keys()}
        self.add_time = {a_name: [] for a_name in algorithms.keys()}
        self.query_time = {a_name: [] for a_name in algorithms.keys()}
        self.query_errors = {a_name: [] for a_name in algorithms.keys()}

    def run_simulation(
        self,
        visualize: bool = True
    ):

        key = None
        if visualize:
            fig = plt.figure(figsize=(20, 10))

        y_original = []

        while key != 'esc' and len(y_original) < self.N:

            new_data_point, timestamp = next(self.generator.simple_data())

            for algo_name, algo in self.algos.items():
                start = time.time()
                algo.add(new_data_point, ts=timestamp)
                self.add_time[algo_name].append(time.time() - start)

            y_original = self.generator.history
            x_original = self.generator.timestamps

            # Get information from algorithms
            # size
            if len(y_original) % 20 == 0:
                for algo_name, algo in self.algos.items():
                    mem = sys.getsizeof(algo)
                    self.memory[algo_name].append(mem)

            # query time and errors
            if len(y_original) > self.n:
                self.queries = {
                    algo_name: [] for algo_name in self.algos.keys()
                }
                for algo_name, algo in self.algos.items():
                    current_time = 0
                    for q10 in range(1, 11):
                        q = q10/10
                        start = time.time()
                        res = algo.query(q=q, last_n=True)
                        current_time += time.time() - start
                        self.queries[algo_name].append(res)
                
                    self.query_time[algo_name].append(current_time/10)
                # take numpy res as true
                true = np.array(self.queries['Numpy'])

                for algo_name in self.algos.keys():
                    err = np.power((true - self.queries[algo_name]), 2)
                    self.query_errors[algo_name].append(np.mean(err))

            # VISUALIZATION PART
            if visualize:
                # create plot image
                if len(y_original) > self.plot_limit:
                    x_plot = x_original[-self.plot_limit:]
                    y_plot = y_original[-self.plot_limit:]
                else:
                    x_plot = x_original
                    y_plot = y_original

                plt.subplot(121)
                plt.title('Original data stream')
                plt.plot(
                    x_plot,
                    y_plot,
                    'o',
                    label='normal'
                )

                plt.plot(
                    x_plot,
                    y_plot,
                    color='black',
                    alpha=0.5,
                    label='normal'
                )

                plt.legend()
                
                plt.subplot(122)
                plt.title('Original data histogram')
                plt.hist(y_original, density=True)

                plt.savefig('temp.png')

                # deal with plot image
                plot_im = cv2.imread('temp.png')

                plot_im = cv2.putText(
                    plot_im,
                    f'Number of points: {len(x_original)}',
                    (40, 40),
                    1, 3, (0, 0, 0),
                    2, cv2.LINE_AA
                )

                # add margin below plot for table
                margin = np.full(
                    (300, plot_im.shape[1], 3),
                    255, dtype=np.uint8
                )

                plot_im = np.concatenate((plot_im, margin), axis=0)

                # generate table
                table = []
                columns = [
                    'algo', 'memory',
                    'add_time', 'query_time',
                    'error'
                ]
                for algo_name in self.algos.keys():
                    row = [algo_name]
                    row.append(np.mean(self.memory[algo_name]))
                    row.append(np.mean(self.add_time[algo_name][-10:]))
                    row.append(np.mean(self.query_time[algo_name][-10:]))
                    row.append(np.mean(self.query_errors[algo_name][-10:]))

                    table.append(row)

                table_str = tabulate(table, headers=columns)
                i = 1
                for row in table_str.split('\n'):
                    plot_im = cv2.putText(
                        plot_im,
                        row,
                        (100, plot_im.shape[1]//2 + i * 50),
                        1, 3, (0, 0, 0),
                        2, cv2.LINE_AA
                    )
                    i += 1


                cv2.imshow('simulation', plot_im)

                key_id = cv2.waitKey(1)
                if key_id not in id2key.keys():
                    key_id = -1

                key = id2key[key_id]

                plt.clf()

        if visualize:
            cv2.destroyAllWindows()


    def generate_report(self) -> Dict:
        return {
            'memory': self.memory,
            'add_time': self.add_time,
            'query_time': self.query_time,
            'query_errors': self.query_errors
        }

