Part 2: Technical Coding Problem
Scenario

You're the engineer responsible for a lightweight internal tool that turns messy weekly quiz-score exports from the LMS into clean, usable student records, then ranks students by performance. The exports are inconsistent on purpose: some rows have malformed score data, some are duplicates. Your tool has to clean what it can, refuse what it can't, and never crash on a single bad row.

Use this raw dataset exactly as given:

raw_rows = [
    {"name": " Amara ", "scores": "92,85,78"},
    {"name": "Leo", "scores": "88,91,73"},
    {"name": "Priya", "scores": "65,72,150"},         
    {"name": "Sam", "scores": "70,not_a_number,60"},  
    {"name": "Amara", "scores": "95,90,88"},          
    {"name": "Jade", "scores": "81,77,84,90"},
]



Each student record has a name and a set of quiz scores, where every score must be a number between 0 and 100 inclusive; a record with no valid scores, or any score outside that range, is invalid and must be rejected with a specific, informative error rather than a generic exception or a silent skip. Once a student record has been built and finalized, it should be treated as locked, and attempting to add another score to a locked record should raise a specific, custom error that clearly identifies which student it happened to and why. Every student also needs a clean, human-readable representation for logging via __str__, along with a separate, unambiguous representation for debugging via __repr__. Because the raw export data isn't clean, it needs to be cleaned in Pandas first: names get trimmed, the scores column (a comma-separated string per row) gets parsed into numeric values, and duplicate names get dropped, keeping the first occurrence — dropped duplicates aren't errors, so they shouldn't appear in the failures list or get printed, and rows that fail to parse shouldn't crash the whole cleaning pass. From there, the cleaned rows still need to become Student objects one at a time, and a row can still fail at this stage too, for instance if a score is out of range; the batch builder must not crash on a single bad row, and should instead collect what fails and why alongside what succeeds. Finally, every student's average score must be computed with a vectorized NumPy operation using np.mean(), not a manual sum-and-divide loop.




Your Task

Write a Python module that defines a Student class with name and scores (stored as a NumPy array), validating the scores on construction per rule 1, and including a .lock() method, an .add_score() method that respects rule 2, and an .average() method built on np.mean(). It should also define two custom exceptions — for example InvalidScoreError and StudentRecordLockedError — that carry enough information for the caller to understand what happened, raised wherever rules 1 and 2 require them, and it should implement __str__ and __repr__ on Student per rule 3. The module needs a single function that handles both cleaning and building in sequence: it cleans raw_rows with Pandas (trimming, parsing, and dropping duplicates) per rule 4, then builds Student objects from what's left per rule 5, using specific exception handling rather than a bare except: at each stage where something can fail. This function should return (students, failures), where failures is a list of {"row": <original raw dict>, "error": <reason>} entries covering both parse failures and validation failures, whichever stage caught them — with dropped duplicates excluded from failures entirely, as rule 4 specifies. Finally, the module should implement a ranking function that uses sorted() with a lambda key to sort students by average score in descending order.




Libraries You'll Need
import pandas as pd
import numpy as np


Beyond that, use whatever's appropriate and there's no fixed list required.




What You Need to Print

Running your script should print, in order:

Each successfully built student via print(student).
The full list of built students in one call, e.g. print(students).
One line per failed row (not including dropped duplicates): Skipped row: {original raw dict} -> reason: {error}.
One manual demonstration: build a valid Student, lock it, attempt .add_score(), catch your custom exception, print it.
The ranked list, averages shown to 2 decimal places: 1. Amara — 85.00 avg.




Submission Instructions

Work in VS Code. Push to your own permanent GitHub repository. Create an exam/ folder at the root containing:

A .py file — your complete, runnable solution, including the __main__ block producing everything above.
A .md file — a short chain-of-thought write-up (Minimum of 50 words) on how you structured the combined clean-and-build function and how you decided what counts as a "failure" at each stage.

Commit with clear messages and push before the deadline.

ANY COMMIT AND PUSH AFTER THE DEADLINE WILL RESULT IN AN AUTOMATIC 0 for Part 2.
--> SUBMIT YOUR REPO LINK <--