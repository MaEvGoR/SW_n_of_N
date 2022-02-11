import time
from structures.sw import SW_n_of_N
from structures.gk import GK
from tqdm import tqdm
import numpy as np


def main():
    data = np.random.normal(0, 1/12, 10000)
    epsilon = 0.000001

    gk = GK(epsilon)
    sw = SW_n_of_N(n=len(data), epsilon=epsilon)

    for p in tqdm(data):
        gk.add(p)
        sw.add(p, time.time())

    nmp_quantile = [np.quantile(data, q/10) for q in range(1, 10)]
    gk_quantile = [gk.get_quantile(q/10) for q in range(1, 10)]
    sw_quantile = [sw.query(q/10) for q in range(1, 10)]

    print(nmp_quantile)
    print(gk_quantile)
    print(sw_quantile)


if __name__ == '__main__':
    main()
