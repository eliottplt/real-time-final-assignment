import numpy as np

values = []

with open("results/execution_times.txt", "r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        line = line.strip().replace("\x00", "")
        if line == "":
            continue
        try:
            values.append(float(line))
        except ValueError:
            pass

data = np.array(values)

minimum = np.min(data)
maximum = np.max(data)
q1 = np.percentile(data, 25)
median = np.median(data)
q3 = np.percentile(data, 75)

wcet = maximum * 1.2

print("Number of measurements:", len(data))
print("Min:", minimum)
print("Q1:", q1)
print("Median (Q2):", median)
print("Q3:", q3)
print("Max:", maximum)
print("WCET with 20% margin:", wcet)