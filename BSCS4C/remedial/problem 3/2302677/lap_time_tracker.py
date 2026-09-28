import numpy as np

class ShapeMismatchError(Exception):
    def __init__(self, message=None):
        super().__init__(message or "Athlete has missing lap data") # just pass the message into base exception class and let it handle the str()


class EmptyLapsError(Exception):
    def __init__(self, message=None):
        super().__init__(message or "Athlete has empty lap data")


class LapTimeTracker():
    def __init__(self, names, times) -> None:
        self.names = np.array(names)
        self.times = np.array(times, dtype=float)

    def __len__(self):
        return self.times.shape[0]

    def __repr__(self):
        return f"LapTimeTracker(n_athletes={len(self)}, n_laps={self.times.shape[1]})"
 
    def average_times(self):
        return self.times.mean(axis=1)
 
    def fastest_lap_per_athlete(self):
        return self.times.min(axis=1)
 
    def flag_slow_laps(self, threshold=60):
        return np.where(self.times > threshold, "SLOW", "FAST")
 
    def normalize_columns(self):
        return (self.times - self.times.mean(axis=0)) / self.times.std(axis=0)


def build_tracker(rows, expected_laps=3):
    failures = []
    athlete_names = []
    athlete_times = []

    for row in rows:
        try:
            laps = row["laps"]
            if len(laps) == 0:
                raise EmptyLapsError()
            if len(laps) != expected_laps:
                raise ShapeMismatchError()
        except (EmptyLapsError, ShapeMismatchError) as e: # Remove redundancy since catching both exceptions trigger same logic
            failures.append({"row": row["athlete"], "error": str(e)})
        else:
            athlete_names.append(row["athlete"])
            athlete_times.append(row["laps"])

    tracker = LapTimeTracker(athlete_names, athlete_times) 

    return tracker, failures

if __name__ == "__main__":
    raw_rows = [
        {"athlete": "Ava", "laps": [61.2, 60.8, 62.1]},
        {"athlete": "Ben", "laps": [58.5, 59.0, 57.9]},
        {"athlete": "Cleo", "laps": [65.0, 64.2]},
        {"athlete": "Drew", "laps": []},
        {"athlete": "Elle", "laps": [60.1, 59.8, 60.5]},
        {"athlete": "Finn", "laps": [63.3, 62.9, 63.7]},
    ]

    tracker, failures = build_tracker(raw_rows)

    print("Tracker representation:\n", repr(tracker))
    print("\n")

    print("List of failures from raw_rows:")
    for fails in failures:
        print(fails)

    print("\n")

    print("List of athlete names:\n", tracker.names)
    print("\n")

    print("List of athlete times:\n", tracker.times)
    print("\n")

    print("List of average times:\n", tracker.average_times())
    print("\n")

    print("List of slow and fast laps:\n", tracker.flag_slow_laps())
    print("\n")

    print("List of z-score normalized columns:\n", tracker.normalize_columns())
    print("\n")
