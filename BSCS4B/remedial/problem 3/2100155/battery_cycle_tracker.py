import numpy as np

class CycleCountMismatchError(Exception):
    pass

class EmptyCycleLogError(Exception):
    pass

class BatteryCycleTracker:
    def __init__(self, robot_ids, cycle_minutes):
        self.robot_ids = robot_ids
        self.cycles = np.array(cycle_minutes, dtype=float)

    def __len__(self):
        return len(self.robot_ids)

    def __repr__(self):
        n_robots, n_cycles = self.cycles.shape
        return f"BatteryCycleTracker(n_robots={n_robots}, n_cycles={n_cycles})"
    def average_cycle_time(self):
        return self.cycles.mean(axis=1)

    def longest_cycle(self):
        return self.cycles.max(axis=1)

    def flag_long_cycles(self, threshold):
        return np.where(self.cycles > threshold, "SLOW_CHARGE" , "NORMAL")

    def normalize_column(self):
        return (self.cycles - self.cycles.mean(axis=0)) / self.cycles.std(axis=0)

def build_tracker(rows, expected_cycles=3):
    robot_ids = []
    cycle_minutes = []
    failures = []

    for row in rows:
        robot = row["robot"]
        cycles = row["cycles"]

        try:
            if len(cycles) == 0:
                raise EmptyCycleLogError(f"{robot} has no recorded cycles")

            if len(cycles) !=expected_cycles:
                raise CycleCountMismatchError(
                    f"{robot} has {len(cycles)} cycles, expected {expected_cycles}"
                )
        except(EmptyCycleLogError, CycleCountMismatchError) as e:
            failures.append({"row": row, "error": str(e)})
            continue

        robot_ids.append(robot)
        cycle_minutes.append(cycles)

    tracker = BatteryCycleTracker(robot_ids, cycle_minutes)
    return tracker, failures

if __name__ == "__main__":
    raw_rows = [
    {"robot": "R-01", "cycles": [42.0, 45.5, 41.2]},
    {"robot": "R-02", "cycles": [50.1, 48.7, 49.9]},
    {"robot": "R-03", "cycles": [39.0, 40.1]},
    {"robot": "R-04", "cycles": []},
    {"robot": "R-05", "cycles": [44.4, 43.8, 45.0]},
    {"robot": "R-06", "cycles": [55.2, 54.8, 56.1]},
]

    tracker, failures = build_tracker(raw_rows, expected_cycles=3)

    print(repr(tracker))

    for fail in failures:
        print(f"Skipped row: {fail['row']} reason: {fail['error']}")

    averages = tracker.average_cycle_time()
    for robot_ids, avg in zip(tracker.robot_ids, averages):
        print(f"{robot_ids}: {avg:.2f} min average")

    flags = tracker.flag_long_cycles(threshold=45.0)
    for robot_ids, robot_flags in zip(tracker.robot_ids, flags):
        print(f"{robot_ids}: {', '.join(robot_flags)}")

