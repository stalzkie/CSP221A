import functools
import logging

logger = logging.getLogger(__name__)

class SignupFormatError(Exception):
    pass

def log_parser(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with {args[0]}")
        result = func(*args, **kwargs)
        logger.info(f"Done with {func.__name__}")
        return result

    return wrapper

@log_parser
def parse_signup_line(line):
    parts = line.split("|")
    if len(parts) != 3:
        raise SignupFormatError(f"Need 3 fields but only got {len(parts)}")

    volunteer_id, shift, raw_skills = parts
    volunteer_id = volunteer_id.strip()
    shift = shift.strip().lower()

    valid_shifts = {"morning", "afternoon", "evening"}
    if shift not in valid_shifts:
        raise SignupFormatError(f"'{shift}' is not a valid shift")

    skills = set()
    for skill in raw_skills.split(","):
        skill = skill.strip().lower()
        if skill:
            skills.add(skill)

    return {
        "id": volunteer_id,
        "shift": shift,
        "skills": skills
    }

def clean_signups(lines):
    for line in lines:
        try:
            yield parse_signup_line(line)
        except SignupFormatError as err:
            print(f"Skipped line: '{line}' -> reason: {err}")

def count_by_shift(signups):
    counts = {}
    for record in signups:
        shift = record["shift"]
        counts[shift] = counts.get(shift, 0) + 1
    return counts

if __name__ == "__main__":
    raw_lines = [
        "V001|morning|setup,registration",
        "V002|afternoon|food",
        "V003|evening|cleanup,setup",
        "V004|night|security",
        "V005|morning|registration,food",
        "V006|afternoon",
        "V007|evening|cleanup",
    ]

    valid_signups = []

    try:
        for signup in clean_signups(raw_lines):
            valid_signups.append(signup)
    except Exception as err:
        print(f"Unexpected error occurred: {err}")
    else:
        print(f"Processed {len(valid_signups)} valid signups.")
    finally:
        print("Signup pass complete.")

    shift_summary = count_by_shift(valid_signups)
    print(shift_summary)

    target_skills = {"setup", "food"}

    matched = sorted(
        [
            volunteer["id"]
            for volunteer in valid_signups
            if volunteer["skills"] & target_skills
        ]
    )
    print(matched)