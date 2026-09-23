import numpy as np

class ShapeMismatchError(Exception):
    pass

class EmptyLapsError(Exception):
 pass

class LapTimeTracker:
    def __init__(self, names, lap_times):
        self.names = np.array(names)
        self.times = np.array(lap_times, dtype=float)

    def __len__(self):
        return len(self.names)

    def __repr__(self):
        n_athletes, n_laps = self.times.shape
        return f"LapTimeTracker(n_athletes={n_athletes}, n_laps={n_laps})"
        
    def average_times(self):
        return self.times.mean(axis=1)

    def fastest_lap_per_athlete(self):
        return self.times.min(axis=1)

    def flag_slow_laps(self, threshold):
        return np.where(self.times > threshold, "SLOW", "FAST")

    def normalize_columns(self):
        return (self.times - self.times.mean(axis=0)) / self.times.std(axis=0)

def build_tracker(rows, expected_laps=3):
    clean_names = []
    clean_laps = []
    skipped_entries = []

    for row in rows:
        try:
            laps = row.get("laps", [])

            if not laps:
                raise EmptyLapsError("Empty log (no recorded laps).")
            if len(laps) != expected_laps:
                raise ShapeMismatchError(
                    f"Shape mismatch: expected {expected_laps} laps, got {len(laps)}."
                )

            clean_names.append(row["athlete"])
            clean_laps.append(laps)
        except (EmptyLapsError, ShapeMismatchError) as err:
            skipped_entries.append({"row": row, "error": str(err)})

    return LapTimeTracker(clean_names, clean_laps), skipped_entries

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
    for fail in failures:
        print(f"Skipped row: {fail['row']} -> reason: {fail['error']}")

    averages = tracker.average_times()
    for name, avg in zip(tracker.names, averages):
        print(f"{name}: {avg:.2f}s average")

    flags = tracker.flag_slow_laps(threshold=61.0)
    for name, row_flags in zip(tracker.names, flags):
        print(f"{name}: {', '.join(row_flags)}")