import numpy as np

class CycleCountMismatchError(Exception):
    def __init__(self, message):
        super().__init__(message)

class EmptyCycleLogError(Exception):
    def __init__(self, message):
        super().__init__(message)

class BatteryCycleTracker():
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __repr__(self):
        pass

def build_tracker(rows, expected_cycles=3):
    failures = []
    tracker = []
    for row in rows:
        try:
            if len(row["cycles"]) == 0:
                error_message = f"Robot {row['robot']} has an empty cycle log."
                failures.append({"row": row, "error": error_message})
                raise EmptyCycleLogError(error_message)
        except EmptyCycleLogError as e:
            print(e)
            continue

        try:
            if len(row["cycles"]) != expected_cycles:
                error_message = f"Robot {row['robot']} has a cycle count mismatch."
                failures.append({"row": row, "error": error_message})
                raise CycleCountMismatchError(error_message)
        except CycleCountMismatchError as e:
            print(e)
            continue

        else:
            tracker.append(row)

    print(tracker)
    print(failures)
    return (tracker, failures)

if __name__ == "__main__":
    raw_rows = [
        {"robot": "R-01", "cycles": [42.0, 45.5, 41.2]},
        {"robot": "R-02", "cycles": [50.1, 48.7, 49.9]},
        {"robot": "R-03", "cycles": [39.0, 40.1]},
        {"robot": "R-04", "cycles": []},
        {"robot": "R-05", "cycles": [44.4, 43.8, 45.0]},
        {"robot": "R-06", "cycles": [55.2, 54.8, 56.1]},
    ]
    build_tracker(raw_rows, expected_cycles=3)
