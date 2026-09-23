import logging 
from functools import wraps

raw_lines = [
    "T001|high|login,auth",
    "T002|medium|billing",
    "T003|low|ui,cosmetic",
    "T004|urgent|payments",
    "T005|high|login,payments",
    "T006|medium",
    "T007|low|ui,auth,login",
]

#R1
class TicketFormatError(Exception):
    """Custom exception for ticket format errors."""
    pass


def ticket_log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Calling %s", func.__name__)

        try:
            result = func(*args, **kwargs)
            logging.info("%s completed successfully", func.__name__)
            return result
        except TicketFormatError as e: 
            logging.info("%s raised TicketFormatError: %s", func.__name__, e)
            raise

    return wrapper 
    
#R2
@ticket_log_function
def parse_ticket_line(line):
    """Parse a single ticket line into its components."""
    parts = line.strip().split('|')

    

    #R3
    if len(parts) != 3:
        raise TicketFormatError(f"Invalid ticket format: {line}")

    #R4
    if parts[1].lower() not in {"low", "medium", "high"}:
        raise TicketFormatError(f"Invalid priority level: {parts[1]} in line: {line}")

    return {
        "ticket_id": parts[0],
        "priority": parts[1],
        "tags": {tag.strip().lower() for tag in parts[2].split(',') if tag.strip()}
    } 

def clean_tickets(lines):
    for line in lines:
        try:
            ticket = parse_ticket_line(line)
            yield ticket
        except TicketFormatError as e:
            print(f"Skipped line: {line!r} -> reason: {e}")

def count_by_priority(tickets):
    priority_count = {}

    for ticket in tickets:
        priority = ticket["priority"]
        priority_count[priority] = priority_count.get(priority, 0) + 1

    return priority_count

tickets = []

try:
    for ticket in clean_tickets(raw_lines):
        tickets.append(ticket)

except TicketFormatError as e:
    print(f"Unexpected error : {e}")

else:
    print(f"Processed {len(tickets)} valid tickets.")
    print("Triage pass complete.")

finally:
    print(count_by_priority(tickets))

    target_tags = {"login", "payments"}

    matching_ids = sorted(
        ticket["ticket_id"]
        for ticket in tickets
        if ticket["tags"] & target_tags
    )

    print(matching_ids)








                                     





    

    
    
