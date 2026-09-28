import numpy as np

#gamiton if error ang cycle na nag log na robot
class EmptyCycleLogError(Exception):
    pass
#gamiton if cycle count doesn't match
class CycleCountMismatchError(Exception):
    pass

class BatteryCycleTracker:

    def __init__(self, robot_ids, cycle_minutes):

        #R5 store robot id as a 2d numpy array
        self.robot_ids = robot_ids
        self.cycles = np.array(cycle_minutes)

    #R6 returning the valid robot count
    def __len__(self):
        return len(self.robot_ids)

    #R6 format the text kung gina print ang class
    def __repr__(self):
        return f"BatteryCycleTracker(n_robots={len(self)}, n_cycles={self.cycles.shape[1]})"

    #R7 per robot is axis=1 so no for loop
    def average_cycle_time(self):
        return self.cycles.mean(axis=1)

    #finding max value per robot
    def longest_cycle(self):
        return self.cycles.max(axis=1)

    #R8 vectorize tag using np.where
    def flag_long_cycles(self, threshold=45.0):
        return np.where(self.cycles > threshold, "SLOW_CHARGE", "NORMAL")

    #R9 normalize per column axis=0
    def normalize_columns(self):
        mean = self.cycles.mean(axis=0)
        std = self.cycles.std(axis=0)
        return (self.cycles - mean) / std

# M1 and M2 function to validate and to build data
def build_tracker(rows, expected_cycles=3):
    robot_ids = []
    cycle_data = []
    failures = []

    for row in rows:
        try:
            robot_id = row["robot"]
            cycles = row["cycles"]

            #validating check
            if len(cycles) == 0:
                raise EmptyCycleLogError("empty log")
            if len(cycles) != expected_cycles:
                raise CycleCountMismatchError(
                    f"expected {expected_cycles} cycles, got {len(cycles)}"
                )

            #kung walang error gadugang sa listahan
            robot_ids.append(robot_id)
            cycle_data.append(cycles)

        #collecting the error without crashing
        except (EmptyCycleLogError, CycleCountMismatchError) as error:
            failures.append({
                "row": row,
                "error": str(error)})

    #creating the new tracker obj using clean data
    return BatteryCycleTracker(robot_ids, cycle_data), failures

if __name__ == "__main__":
    raw_rows = [
        {"robot": "R-01", "cycles": [42.0, 45.5, 41.2]},
        {"robot": "R-02", "cycles": [50.1, 48.7, 49.9]},
        {"robot": "R-03", "cycles": [39.0, 40.1]},
        {"robot": "R-04", "cycles": []},
        {"robot": "R-05", "cycles": [44.4, 43.8, 45.0]},
        {"robot": "R-06", "cycles": [55.2, 54.8, 56.1]},
    ]
    #to run the build_tracker
    tracker, failures = build_tracker(raw_rows)

    #printing the tracker
    print(repr(tracker))
    print()

    #printing skipped rows
    for fail in failures:
        print(
            f"Skipped row: {fail['row']} - "
            f"reason {fail['error']}"
              )
    print()

    #printing every robot average
    averages = tracker.average_cycle_time()
    for robot, avg in zip(tracker.robot_ids, averages):
        print(f"{robot}: {avg:.2f} min average")
    print()

    #printing the "SLOW_CHARGE" / "NORMAL" flags
    flags = tracker.flag_long_cycles()
    for robot_id, robot_flags in zip(tracker.robot_ids, flags):
        print(f"{robot_id}: {', '.join(robot_flags)}")