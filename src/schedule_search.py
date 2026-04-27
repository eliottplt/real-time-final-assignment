import subprocess

# Compile C++
subprocess.run(["g++", "src/task1.cpp", "-O2", "-o", "task1"], check=True)

# Execute and capture WCET
result = subprocess.run(["./task1"], capture_output=True, text=True)

lines = result.stdout.strip().split("\n")
wcet_value = float(lines[-1])

print("WCET from C++:", wcet_value)

tasks = [
    ("t1", wcet_value, 10),
    ("t2", 3, 10),
    ("t3", 2, 20),
    ("t4", 2, 20),
    ("t5", 2, 40),
    ("t6", 2, 40),
    ("t7", 3, 80),
]

hyperperiod = 80

jobs = []

for task, C, T in tasks:
    job_number = 1
    for release in range(0, hyperperiod, T):
        jobs.append({
            "id": f"{task}_{job_number}",
            "task": task,
            "C": C,
            "release": release,
            "deadline": release + T,
        })
        job_number += 1


def non_preemptive_edf(jobs):
    time = 0
    remaining = jobs.copy()
    schedule = []

    while remaining:
        available = [j for j in remaining if j["release"] <= time]

        if not available:
            next_release = min(j["release"] for j in remaining)
            schedule.append({
                "id": "IDLE",
                "start": time,
                "finish": next_release,
                "release": time,
                "deadline": next_release,
                "C": next_release - time,
                "waiting": 0,
                "response": 0,
                "deadline_miss": False,
            })
            time = next_release
            continue

        job = min(available, key=lambda j: (j["deadline"], j["release"], j["id"]))

        start = time
        finish = start + job["C"]
        waiting = start - job["release"]
        response = finish - job["release"]
        deadline_miss = (finish > job["deadline"]) and (job["task"] != "t5")

        schedule.append({
            **job,
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "response": response,
            "deadline_miss": deadline_miss,
        })

        time = finish
        remaining.remove(job)

    return schedule


schedule = non_preemptive_edf(jobs)

total_waiting = sum(j["waiting"] for j in schedule if j["id"] != "IDLE")
idle_time = sum(j["finish"] - j["start"] for j in schedule if j["id"] == "IDLE")
misses = [j for j in schedule if j["deadline_miss"]]

print("Schedule:")
for j in schedule:
    print(
        f"{j['id']:6s} "
        f"start={j['start']:6.2f} "
        f"finish={j['finish']:6.2f} "
        f"deadline={j['deadline']:6.2f} "
        f"waiting={j['waiting']:6.2f} "
        f"response={j['response']:6.2f} "
        f"miss={j['deadline_miss']}"
    )

print()
print("Total waiting time:", round(total_waiting, 2))
print("Total idle time:", round(idle_time, 2))
print("Deadline misses:", len(misses))