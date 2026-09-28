import numpy as np

class ShapeMismatchError(Exception):    
    pass

class EmptyLapsError(Exception):
    pass

class LapTimeTracker:
    def __init__(self, name, lap_times):
        self.name = lap_times
        self.name = name
        self.times = np.array(lap_times, dtype=float)

    def __len__(self):
        return len(self.names)

    def __repr__(self):
        n_athletes, n_laps = self.times.shape
        return f"LapTimeTracker(athletes={n_athletes}, laps_per_athlete={n_laps})"

    def avarage_time(self):
        return self.times.mean(axis=1)
    
    def fastest_lap_per_athlete(self):
        return self.times.min(axis=1)

    def flag_slow_laps(self,threshold):
        return np.where(self.times > threshold, "SLOW", "FAST")

    def normalize_colums(self):
        col_means = self.times.mean(axis=0)
        col_stds = self.times.std(axis=0)
        return (self.times - col_means) / col_stds
    
def build_tracker(rows, expected_laps=3):
    valid_names = []
    valid_laps = []
    failures = []

    for row in rows:
        try:
            laps = row.get("laps", [])

            if len(laps) == 0:
                raise EmptyLapsError("Empty lap log")
            if len(laps) != expected_laps:
                raise ShapeMismatchError(
                    f"Expected {expected_laps} laps, got {len(laps)}"
                )
            
            valid_names.append(row["athlete"])
            valid_laps.append(laps)

        except (EmptyLapsError, ShapeMismatchError) as err:
            failures.append({"row": row, "error": str(err)})

    tracker = LapTimeTracker(valid_names, valid_laps)
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

    tracker, failures = build_tracker(raw_rows, expected_laps=3)
    print(repr(tracker))
    print()

    for failure in failures:
        print(
            f"Skipped row: {failure['row']} -> reason: {failure['error']}"
        )
    print()

    averages = tracker.avarage_time()
    for name, avg in zip(tracker.name, averages):
        print(f"{name}: {avg:.2f}s average")
    print()

    flags = tracker.flag_slow_laps(61.0)
    for name, athlete_flags in zip(tracker.name, flags):
        flags_str = ", ".join(athlete_flags)
        print(f"{name}: {flags_str}")

