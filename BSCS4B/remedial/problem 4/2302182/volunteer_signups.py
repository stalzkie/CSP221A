import logging
from functools import wraps


logging.basicConfig(level=logging.INFO)


raw_lines = [
    "V001|morning|setup,registration",
    "V002|afternoon|food",
    "V003|evening|cleanup,setup",
    "V004|night|security",
    "V005|morning|registration,food",
    "V006|afternoon",
    "V007|evening|cleanup",
]


class SignupFormatError(Exception):
    pass


def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Starting: {func.__name__}...")
        try:
            result = func(*args,**kwargs)
            return result
        finally:
            logging.info(f"Finished: {func.__name__}...")
    return wrapper


@log_action
def parse_signup_line(line):
    parts = line.split("|")
    if len(parts) != 3:
        raise SignupFormatError(f"3 parts is expected, but got {len(parts)}")
    
    volunteer_id, shift, skills_raw =  parts
    shift = shift.lower()
    if shift not in {"morning", "afternoon", "evening"}:
        raise SignupFormatError(f"{shift} is an INVALID shift")
    
    skills = {skill.strip().lower() for skill in skills_raw.split(",")}
    
    return {
        "id": volunteer_id,
        "shift": shift,
        "skills": skills
    }


def clean_signups(lines):
    for line in lines:
        try:
            signup = parse_signup_line(line)
        except SignupFormatError as e:
            print(f"Skipped line: '{line}' -> reason: {e}")
        else:
            yield signup


def count_by_shift(signups):
    counts = {}
    
    for signup in signups:
        shift = signup["shift"]
        counts[shift] = counts.get(shift, 0) + 1
    
    return counts


signups = []

try:
    signups = list(clean_signups(raw_lines))
except Exception as e:
    print(f"An unexpected error: {e}")
else:
    print(f"Processed {len(signups)} valid signups.")
finally:
    print("Signup pass complete.")

print(count_by_shift(signups))

target_skills = {"setup", "food"}

matching_ids = []

for signup in signups:
    if signup["skills"] & target_skills:
        matching_ids.append(signup["id"])

matching_ids = sorted(matching_ids)
print(matching_ids)