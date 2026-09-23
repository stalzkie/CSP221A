import numpy as np

class ShapeMismatchError(Exception):
    pass

class EmptyLapsError(Exception):
    pass

class LapTimeTracker:

    def __init__(self, names, lap_times):
        self.names = names
        self.times = lap_times

    def __len__(self):
        return len(self.names)

    def __repr__ (self):
        return f"LapTimeTracker (n_athletes={len(self)}), n_laps={self.times.shape[1]} "

    def average_time(self):
        return self.times.mean(axis = 1)

    def fastest_lap_per_athlete(self):
        return self.times.min(axis = 1)

    def flag_slow_laps(self, threshold):
        return np.where(self.times > threshold, "SLOW", "FAST")

    def normalize_columns(self):
        return (
            self.times - self.times.mean(axis = 0) )/ self.times.std(axis = 0)

    def build_tracker(rows, expected_laps = 3):
        names = []
        lap_times = []
        failures = []

        for row in rows:
            try:
                laps = row ["laps"]

                if len(laps) == 0:
                    raise EmptyLapsError("No laps recorded")

                if len(laps) !=expected_laps:
                    raise ShapeMismatchError ("Wrong number of laps")

                names.append(row["athlete"])
                lap_times.append(laps)

            except EmptyLapsError as error:
                failures.append({
                    "row": row,
                    "error": str(error)
                })

            except ShapeMismatchError as error:
                failures.append({
                    "row": row,
                    "error": str(error)
                })

        tracker = LapTimeTracker(names, np.array(lap_times))

        return tracker, failures

raw_rows = [
    {"athlete": "Ava", "laps": [61.2, 60.8, 62.1]},
    {"athlete": "Ben", "laps": [58.5, 59.0, 57.9]},
    {"athlete": "Cleo", "laps": [65.0, 64.2]},
    {"athlete": "Drew", "laps": []},
    {"athlete": "Elle", "laps": [60.1, 59.8, 60.5]},
    {"athlete": "Finn", "laps": [63.3, 62.9, 63.7]},
]

tracker, failures = LapTimeTracker.build_tracker(raw_rows)

print(tracker)

for failure in failures:
    print(
        "Skipped row:",
        failure ["row"],
        "reason:",
        failure["error"]
    )

average = tracker.average_time()

for i in range(len(tracker)):
    print(f"{tracker.names[i]}: {average[i]:.2f}s average")
flags = tracker.flag_slow_laps(61.0)

for i in range(len(tracker)):
    print(f"{tracker.names[i]}: {flags[i][0]}, {flags [i][1]}, {flags [i][2]}")