import numpy as np

class ShapeMismatchError(Exception):
    def __init__(self, athlete_name):
        message = f"Incomplete laps."
        super().__init__(message)
        self.athlete_name = athlete_name

class EmptyLapsError(Exception):
    def __init__(self, athlete_name):
        message = f"No laps recorded."
        super().__init__(message)
        self.athlete_name = athlete_name

class LapTimeTracker:
    def __init__(self, name, lap_times):
        self.name = name
        self.times = np.array(lap_times)

    def __len__(self):
        return self.times.shape[0]

    def __repr__(self):
        n_athletes, n_laps = self.times.shape
        return f"LapTimeTracker(n_athletes={n_athletes}, n_laps={n_laps})"

    def average_times(self):
        return self.times.mean(axis = 1)

    def fastest_lap_per_athlete(self):
        return self.times.min(axis = 1)

    def flag_slow_laps(self, threshold):
        return np.where(self.times > threshold, "SLOW", "FAST")

    def normalize_columns(self):
        return(self.times - self.times.mean(axis = 0)) / self.times.std(axis = 0)

def build_tracker(rows, expected_laps = 3):
    names = []
    lap_times = []
    failures = []

    for row in rows:
        athlete_name = row.get("athlete")
        athlete_laps = row.get("laps", [])

        try:
            if len(athlete_laps) == 0:
                raise EmptyLapsError(athlete_name)
                continue

            if len(athlete_laps) != expected_laps:
                raise ShapeMismatchError(athlete_name)
                continue

        except (EmptyLapsError, ShapeMismatchError) as e:
            failures.append({"Row": row, "Error": str(e)})
            continue

        names.append(athlete_name)
        lap_times.append(athlete_laps)

    tracker = LapTimeTracker(names, lap_times)
    return tracker, failures

raw_rows = [
    {"athlete": "Ava", "laps": [61.2, 60.8, 62.1]},
    {"athlete": "Ben", "laps": [58.5, 59.0, 57.9]},
    {"athlete": "Cleo", "laps": [65.0, 64.2]},
    {"athlete": "Drew", "laps": []},
    {"athlete": "Elle", "laps": [60.1, 59.8, 60.5]},
    {"athlete": "Finn", "laps": [63.3, 62.9, 63.7]},
]

if __name__ == "__main__":
    tracker, failures = build_tracker(raw_rows, expected_laps = 3)

    averages = tracker.average_times()
    flags = tracker.flag_slow_laps(threshold = 61.0)

    print(tracker)
    print("\nSkipped Rows:")
    for failure in failures:
        print(failure)

    print("\nAverage lap times:")
    for name, avg in zip(tracker.name, averages):
        print(f"{name}: {avg:.2f} seconds")

    print("\nSlow/fast laps:")

    for name, row in zip(tracker.name, flags):
        print(f"{name}: {row}")