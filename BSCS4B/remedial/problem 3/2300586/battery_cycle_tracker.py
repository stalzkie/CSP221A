import numpy as np

class CycleCountMismatchError(Exception):
    """This custom exception error is raised when the robot's cycle count does not match expected cycles which is 3."""
    pass

class EmptyCycleLogError(Exception):
    """This custom exception error is raised when a robot has no recorded charge cycle."""
    pass

def build_tracker(rows, expected_cycles = 3):
    valid_rows = []
    failures = []

    for row in rows:
        try:
            cycles = row["cycles"]
            if len(cycles) == 0:
                raise EmptyCycleLogError(f"Robot has no recorded charge cycle.")

            if len(cycles) != expected_cycles:
                raise CycleCountMismatchError(f"Expected cycle count is {expected_cycles}")

            valid_rows.append(row)

        except (EmptyCycleLogError, CycleCountMismatchError) as error:
            failures.append({"row": row, "error": str(error)})

    robot_ids = [r["robot"] for r in valid_rows]
    cycle_minutes = [r["cycles"] for r in valid_rows]

    tracker = BatteryCycleTracker(robot_ids, cycle_minutes)
    return tracker, failures 

class BatteryCycleTracker:
    def __init__(self, robot_ids, cycle_minutes):
        self.robot_ids = robot_ids
        self.cycles = np.array(cycle_minutes, dtype=float)

    def __len__(self):
        return(len(self.robot_ids))

    def __repr__(self):
        n_robots, n_cycles = self.cycles.shape
        return f"BatteryCycleTracker(n_robots={n_robots}, n_cycles={n_cycles})"

    def average_cycle_time(self):
        return self.cycles.mean(axis=1)

    def longest_cycle(self):
        return self.cycles.max()

    def flag_long_cycles(self, threshold):
        return np.where(self.cycles > threshold, "SLOW_CHARGE", "NORMAL")

    def normalize_columns(self):
        return (self.cycles - self.cycles.mean(axis=0)) / self.cycles.std(axis=0)

if __name__== "__main__":
    raw_rows = [
    {"robot": "R-01", "cycles": [42.0, 45.5, 41.2]},
    {"robot": "R-02", "cycles": [50.1, 48.7, 49.9]},
    {"robot": "R-03", "cycles": [39.0, 40.1]},
    {"robot": "R-04", "cycles": []},
    {"robot": "R-05", "cycles": [44.4, 43.8, 45.0]},
    {"robot": "R-06", "cycles": [55.2, 54.8, 56.1]},
]

    tracker, failures = build_tracker(raw_rows)
    print(repr(tracker))

    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")

    for robot_id, avg in zip(tracker.robot_ids, tracker.average_cycle_time()):
        print(f"{robot_id}: {avg:.2f} min average")

    flag_matrix = tracker.flag_long_cycles(45.0)
    for robot_id, flags in zip(tracker.robot_ids, flag_matrix):
        print(f"{robot_id}: {', '.join(flags)}")
