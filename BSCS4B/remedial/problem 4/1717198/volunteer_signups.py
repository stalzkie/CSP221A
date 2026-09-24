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

Allowed_shifts = {"morning", "afternoon", "evening"}

class SignupFormatError(Exception):
    pass #this catches all the errors?

#decorator using wraps 
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call  
def parse_signup_line(line):
    parts = line.split("|")
    if(len(parts) != 3):
        raise SignupFormatError("The length is not equals to 3")
    volunteer_id, shift, skills = parts

    shift = shift.strip().lower()

    if(shift not in Allowed_shifts):
        raise SignupFormatError("The shift is not in the allowed shifts")        

    cleaned_skills = {s.strip().lower() for s in skills.split(",")} #this loops the split in skills to set 
    #dic...tionary
    return {"volunteer_id":volunteer_id.strip(), "shift":shift, "skills":cleaned_skills}

#generator
def clean_signups(lines): 
    for line in lines: 
        try: 
            parsed_data = parse_signup_line(line)
            yield parsed_data
        except SignupFormatError as e: 
            print(f"Skipped line: {line!r} -> reason: {e}")
    
def count_by_shift(signups):
    count = {} #empty dictionary to store the shifts
    for signup in signups:
        shift = signup["shift"]
        count[shift] = count.get(shift, 0) + 1
    return count

#M4, matches the id with skills 
def skill_look_up(signups, target_skills): 
    matched_volunteers = []

    for signup in signups: 
        if signup["skills"] & target_skills: 
            matched_volunteers.append(signup["volunteer_id"])
    return sorted(matched_volunteers)

count = 0 
valid_signups = []

try:
    for signup in clean_signups(raw_lines):
        count += 1 
        valid_signups.append(signup)

except SignupFormatError as e: 
    print(f"Error occured when cleaning signups: {e}")

else: 
    print(f"Processed {count} valid signups.")
    
finally: 
    print("Signup pass complete.")

shift_counts = count_by_shift(valid_signups)
print(shift_counts)
target_skills = {"setup", "food"}
matched_volunteers = skill_look_up(valid_signups, target_skills)
print(matched_volunteers)


    