import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

def moving_average(x, w):
    return np.concatenate((np.zeros(w), np.convolve(x, np.ones(w), 'valid') / w))

def main(args):
    path = args.report

    with open(path) as f:
        data = json.load(f)
    
    for metric_name, algos in data.items():
        plt.figure(figsize=(10, 10))

        for idx, (algo_name, values) in enumerate(algos.items()):

            ma = moving_average(values, 50)

            plt.subplot(2, 2, idx + 1)
            plt.title(f'{algo_name} - {metric_name}')

            plt.plot(np.log(values), label='original', alpha=0.7)
            plt.plot(np.log(ma), label='ma')
            plt.legend()

            plt.subplot(2, 2, 4)
            plt.plot(np.log(values), label=algo_name)
        
        plt.subplot(2, 2, 4)
        plt.title('all')
        plt.legend()

        plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-r',
        '--report',
        type=str,
        default='report.json',
        help='Path to report file'
    )

    args = parser.parse_args()
    main(args)