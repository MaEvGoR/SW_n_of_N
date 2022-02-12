from os import times
import numpy as np
import time
import random

class Generator():

    def __init__(
        self,
        seed = 2022
    ):
        self.seed = seed
        self.history = []
        self.timestamps = []

    def simple_data(
        self,
        mean=0,
        std=1/12,
        n=1000,
        delay=True
    ):
        if delay:
            self.delay()

        sample = np.random.normal(mean, std)
        timestamp = time.time()

        self.history.append(sample)
        self.timestamps.append(timestamp)

        yield (sample, timestamp)

    def delay(self):
        # random delay between 0 and 1 second
        delay_time = random.randint(0, 3)/10
        time.sleep(delay_time)
