import numpy as np
import time

class Timer:

    def __init__(self, func):
        self.func = func
        self.count = 0
        self.total = 0
        self.min = np.inf
        self.max = -np.inf

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        end = time.time()
        elapsed = end - start

        self.count += 1
        self.min = min(self.min, elapsed)
        self.max = max(self.max, elapsed)
        self.total += elapsed
        return result

    def timer_print(self):
        print(f"Function: {self.func.__name__}")
        if self.count == 0:
            print("  No calls")
            return

        avg = self.total / self.count
        print(f"  Number of calls: {self.count}")
        print(f"     Average time: {avg}")
        print(f"         Min time: {self.min}")
        print(f"         Max time: {self.max}")


@Timer
def example_numpy(n):
    x = np.random.rand(n, n, n)
    x = np.fft.fft(x)

for i in range(10):
    example_numpy(200)

example_numpy.timer_print()

