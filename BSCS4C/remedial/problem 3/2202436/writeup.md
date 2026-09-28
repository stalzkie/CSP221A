#Remedial Problem 3: Vectorization Expalnation

The calculations in `average_time()`, `flag_slow_laps()`and `normallize_columns()` are vectorized because they perform array-wide opperations directly in compiled C code without relying on explicit Python `for` loops.

In the `self.time.mean(axix=1)` computes all athlete averages accros columms in a single vectorized call.

In the `np.where(self.times > threshold, "SLOW", "FAST")` evaluates every lap simultaneously using conditional array indexing.

In the `normalize_columns()` uses array broadcasting to subtract 1D column means for a 2D matrix automatically.

If we weren't careful using standard Python loops (like `[sum(row)/len(row) for row in self.times]`) or mixing multidemensional arrays with inconsistent row lengths ragge arrays would force Python elements sequentially in interpreted memory, breaking vectorization and introducing performance bottlenecks.
