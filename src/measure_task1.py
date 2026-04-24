import subprocess
import time
import numpy as np
from pathlib import Path

N = 1000
EXE = ".\\task1.exe"

times = []

for i in range(N):
    start = time.perf_counter()
    subprocess.run(EXE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    end = time.perf_counter()
    times.append(end - start)

data = np.array(times)

minimum = np.min(data)
q1 = np.percentile(data, 25)
median = np.median(data)
q3 = np.percentile(data, 75)
maximum = np.max(data)
wcet = maximum * 1.2

Path("results").mkdir(exist_ok=True)

with open("results/task1_timing_stats.txt", "w") as f:
    f.write(f"Number of measurements: {N}\n")
    f.write(f"Min: {minimum}\n")
    f.write(f"Q1: {q1}\n")
    f.write(f"Median Q2: {median}\n")
    f.write(f"Q3: {q3}\n")
    f.write(f"Max: {maximum}\n")
    f.write(f"WCET with 20% margin: {wcet}\n")

np.savetxt("results/task1_execution_times.txt", data)

print("Number of measurements:", N)
print("Min:", minimum)
print("Q1:", q1)
print("Median Q2:", median)
print("Q3:", q3)
print("Max:", maximum)
print("WCET with 20% margin:", wcet)