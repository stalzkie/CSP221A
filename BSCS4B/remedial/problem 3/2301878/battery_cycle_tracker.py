import numpy as np

class CycleCountMismatchError(Exception):
    """Raised when a robot does not have the expected number of cycles."""
    def __init__(self, message="Cycle count mismatch error"):
        self.message = message
        super().__init__(self.message)
        

class EmptyCycleLogError(Exception):
    """Raised when a robot has an empty cycle count."""
    def __init__(self, message="Empty cycle count error"):
        self.message = message
        super().__init__(self.message)
        


class BatteryCycleTracker:
    def __init__(self, robot_id, cycle_time):
        self.robot_id = list(robot_id)  # Convert robot_id to a list
        self.cycles = np.array(cycle_time, dtype=float)  # Convert cycle_time to a numpy array

        if self.cycles.shape[0] == 0:
            raise EmptyCycleLogError("Cycle log cannot be empty.")
        
        if len(self.robot_id) != self.cycles.shape[0]:
            raise CycleCountMismatchError("Robot ID and cycle count must have the same length.")
        
    def __len__(self):
            return len(self.robot_id)
        
    def __repr__(self):
            return (
                    f"BatteryCycleTracker("
                    f"n_robot={len(self.robot_id)}, "
                    f"n_cycle={self.cycles.shape[1]})"
                    )
                
        
    def average_cycle_time(self):
        """Return each robot's average cycle time using vectorized NumPy math."""
        return self.cycles.mean(axis=1)

    def longest_cycle(self):
        """Return the longest recorded cycle for each robot."""
        return self.cycles.max(axis=1)

    def flag_long_cycles(self, threshold):
        """Label every cycle as SLOW_CHARGE or NORMAL in one vectorized call."""
        return np.where(self.cycles > threshold, "SLOW_CHARGE", "NORMAL")

    def normalize_columns(self):
        """Z-score each cycle column across all valid robots using broadcasting."""
        return (
            (self.cycles - self.cycles.mean(axis=0))
            / self.cycles.std(axis=0)
        )
        
        
def build_tracker(rows, expected_cycles=3):
    robot_id = []
    cycle_times = []
    failed_robots = []
    
    for row in rows:
        try:
            cycles = row["cycles"]
            robot = row["robot"]
            
            if len(cycles) == 0:
                raise EmptyCycleLogError(f"Robot {robot} has an empty cycle log.")
            
            if len(cycles) != expected_cycles:
                raise CycleCountMismatchError(f"Robot {robot} has a cycle count mismatch.")
            
            robot_id.append(robot)
            cycle_times.append(cycles)
            
        except (EmptyCycleLogError, CycleCountMismatchError) as error:
            failed_robots.append({
                "row": row,
                "error": str(error)
            })
      
      
            
    tracker = BatteryCycleTracker(robot_id, cycle_times)
    return tracker, failed_robots
    
    
    
if __name__ == "__main__":
    rows = [
    {"robot": "R-01", "cycles": [42.0, 45.5, 41.2]},
    {"robot": "R-02", "cycles": [50.1, 48.7, 49.9]},
    {"robot": "R-03", "cycles": [39.0, 40.1]},
    {"robot": "R-04", "cycles": []},
    {"robot": "R-05", "cycles": [44.4, 43.8, 45.0]},
    {"robot": "R-06", "cycles": [55.2, 54.8, 56.1]},
    ]
    
    tracker, failed_robots = build_tracker(rows)
    
    print(repr(tracker))
    
    print("\nFailed Robots:")
    for failed_robot in failed_robots:
        print(
            f"Failed Robot: {failed_robot['row']}, "
            f"Error: {failed_robot['error']}"
        )

    print("\nAverage Cycle Times:")
    averages = tracker.average_cycle_time()

    for robot_id, average in zip(tracker.robot_id, averages):
        print(
            f"Robot: {robot_id}, "
            f"Average Cycle Time: {average:.2f} min average"
        )

    print("\nLongest Cycle:")
    longest = tracker.longest_cycle()

    for robot_id, cycle in zip(tracker.robot_id, longest):
        print(
            f"Robot: {robot_id}, "
            f"Longest Cycle: {cycle:.2f}"
        )

    print("\nCycle Flags:")
    flags = tracker.flag_long_cycles(threshold=45.0)

    for robot_id, flag in zip(tracker.robot_id, flags):
        print(f"Robot: {robot_id}, Cycle Flag: {flag}")

    print("\nNormalized Columns:")
    print(tracker.normalize_columns())