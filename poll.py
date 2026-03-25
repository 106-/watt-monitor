import time

import sensor
from sensor import rms_power_test

print(f"Warmup done: bias = {sensor.bias:.6f}")

count = 0
rate = 0.0
t0 = time.time()

while True:
    power, n_samples = rms_power_test()
    count += 1

    now = time.time()
    elapsed = now - t0
    if elapsed >= 1.0:
        rate = count / elapsed
        count = 0
        t0 = now

    print(f"\rPower: {power:8.1f} W  |  {rate:5.1f} meas/s  |  {n_samples} samples/meas", end="", flush=True)
