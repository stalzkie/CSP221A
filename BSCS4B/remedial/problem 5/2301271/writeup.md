*How do you decide whether a row counts as a failure*
*or just messy but fixable*

In cleaning the employee training logs, rows were categorized as fixable if the
core metrics were not missing or mangled beyond fixing. This category includes
those with formatting issues like irregular whitespace and inconsistent capitalization, which could easily be solved by normalization using `.str.strip().str.lower()`. Duplicate data could 
also just be easily dropped without affecting the results.

Row 4 (E04), however, contained an unparseable "N/A" string in the training hours column, which is missing and unrecoverable data. Training hours is an important metric and other derived columns depend on it; it is used to categorize employee progress and evaluate status thresholds. Therefore, ignoring missing hours would greatly affect the audit's integrity, making dropping the row necessary. 