import numpy as np
class ShapeMismatchError(Exception):
    pass
class EmptyLapsError(Exception):
    pass

def build_tracker(rows, expected_laps=3):
    names = []
    lap_times = []
    failures = []

    for row in rows:
        try:
            laps = row["laps"]

            if len(laps) == 0:
                raise EmptyLapsError(f"EmptyLapsError:{row['athlete']} has 0 laps")

            if len(laps) != expected_laps:
                raise ShapeMismatchError(f"ShapeMismatchError:{row['athlete']}  has {len(laps)} laps when it is expected {expected_laps}")
            names.append(row["athlete"])
            lap_times.append(laps)

        except EmptyLapsError as error:
            print(f"Skipped row: {row}, {error}")

        except ShapeMismatchError as error:
            print(f"Skipped row: {row}, {error}")

    tracker = LaptimeTracker(names, lap_times)

    return tracker, failures

class LaptimeTracker:
    def __init__(self, names, lap_times):
        self.names = names
        self.times = np.array(lap_times, dtype=float)

    def __len__(self):
        return len(self.names)

    def __repr__(self):
        n_athletes = len(self.names)
        n_laps = self.times.shape[1]

        return (
            f"\n{n_athletes} valid athletes\n{n_laps} laps each"
        )

    def average_times(self):
        return self.times.mean(axis=1)

    def flag_slow_laps(self, threshold):
        return np.where(self.times > threshold, "SLOW", "FAST")

    def fastest_lap_per_athlete(self):
        return self.times.min(axis=1)

    def normalize_columns(self):
        return (
            (self.times - self.times.mean(axis=0)) / self.times.std(axis=0)
        )
        

raw_rows = [
    {"athlete": "Ava", "laps": [61.2, 60.8, 62.1]},
    {"athlete": "Ben", "laps": [58.5, 59.0, 57.9]},
    {"athlete": "Cleo", "laps": [65.0, 64.2]},
    {"athlete": "Drew", "laps": []},
    {"athlete": "Elle", "laps": [60.1, 59.8, 60.5]},
    {"athlete": "Finn", "laps": [63.3, 62.9, 63.7]},
]


print(f"\n1.")
tracker, failures = build_tracker(raw_rows)

#1. `repr(tracker)`.
print(repr(tracker))
print(f"\n2.")

#2. One line per skipped row: `Skipped row: {original raw dict} -> reason: {error}`.
for failure in failures:
    print(f"Skipped: {failure['row']} -> reason {failure['error']}")


print(f"\n3.")

#3. Each athlete's average lap time: `Ava: 61.37s average`.
averages = tracker.average_times()

for name, average in zip(tracker.names, averages):
    print(f"{name}: {average:.2f}s average")

print(f"\n4.")

#4. Each athlete's SLOW/FAST flags (threshold 61.0): `Ava: SLOW, FAST, SLOW`.
flags = tracker.flag_slow_laps(61.0)

for name, athlete_flags in zip(tracker.names, flags):
    print(f"{name}: {', '.join(athlete_flags)}")

print(f"\n")