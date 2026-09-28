#ID V004 is rejected because it is not a valid shift which will be 'rejected'. Use only 'morning', 'afternoon', or 'evening' as valid shifts.
#ID V006 only has two inputs and missing the skill field which will be 'rejected'. Use the format: ID, Shift, Skill.
#`SignupFormatError(Exception)` is defined and used for every rejection below.


import logging
import functools


#rule 1: Used fpr every rejection
class SignupFormatError(Exception):
    pass

#rule 5: decoter w/ logging decorator, uses `functools.wraps` so the wrapped function keeps its real `__name__`
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        line = args[0] if args else kwargs.get("line")
        print(f"[LOG] Checking {func.__name__} with: {line}")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished {func.__name__} : {result}")
        return result
    return wrapper
    

@log_calls
#rule 2: plits on `"|"` and raises `SignupFormatError` if it doesn't get exactly 3 parts.
def parse_signup_line(line):
    parts = line.split('|')
    if len(parts) != 3:
        raise SignupFormatError(f"Invalid format: {line}")

    id, shift, skill = parts[0].strip(), parts[1].strip(), parts[2].strip()

#rule 3: parse_signup_line(line)` raises `SignupFormatError` if the shift (lowercased) isn't one of `{"morning", "afternoon", "evening"}`.
    if shift not in ['morning', 'afternoon', 'evening']:
            raise SignupFormatError(f"Invalid shift: {shift}")
    shift = shift.lower()

#rule 4: Skills are parsed into a **set** of lowercased, stripped strings
    skills = {s.strip().lower() for s in skill.split(',') if s.strip()}
    if not skills:
            raise SignupFormatError(f"Invalid skill: {skill}")

    return {
            "id": id,
            "shift": shift,
            "skills": skills
        }

#rule 6: a **generator** (uses `yield`) cleaned signup dicts, printing a skip message
def clean_signups(lines):
    for line in lines:
        try:
            yield parse_signup_line(line)
        except SignupFormatError as e:
            print(f"[ERROR] Skipping line due to: {e}")


#rule 8: `count_by_shift(signups)` builds its counts using a dict and `.get()`
def count_by_shift(signups):
    counts = {}
    for signup in signups:
        shift = signup['shift']
        counts[shift] = counts.get(shift, 0) + 1
    return counts

        
raw_lines = [
    "V001|morning|setup,registration",
    "V002|afternoon|food",
    "V003|evening|cleanup,setup",
    "V004|night|security",
    "V005|morning|registration,food",
    "V006|afternoon",
    "V007|evening|cleanup",
]

#rule 7:The main flow uses a full `try/except/else/finally` around consuming the generator.
valid_signups = []
try:
     for signup in clean_signups(raw_lines):
            valid_signups.append(signup)
except Exception as e:
     print(f"An error occurred: {e}")
else:
     print("All signups processed successfully.")
finally:
     print("Finished processing signups.")

print(count_by_shift(valid_signups))