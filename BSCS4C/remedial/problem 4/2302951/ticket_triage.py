import functools
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class TicketFormatError(Exception):
    """Custom exception for malformed ticket lines."""
    pass

def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Finished {func.__name__}")
            return result
        except Exception as e:
            logging.warning(f"Error in {func.__name__}: {e}")
            raise e
    return wrapper   

@log_execution
def parse_ticket_line(line):
    parts = line.strip().split("|")
    if len(parts) != 3:
        raise TicketFormatError(f"Expected 3 pipe-separated fields, got {len(parts)}")

    ticket_id, priority, tags_str = parts
    priority = priority.lower()

    valid_priorities = {"low", "medium", "high"}
    if priority not in valid_priorities:
        raise TicketFormatError(f"Invalid priority '{priority}'. Must be low, medium, or high.") 

    tags = {tag.strip().lower() for tag in tags_str.split(",") if tag.strip()}

    return {
        "id": ticket_id,
        "priority": priority,
        "tags": tags
    }

def clean_tickets(lines):
    for line in lines:
        try:
            ticket = parse_ticket_line(line)
            yield ticket
        except TicketFormatError as e:
            print(f"Skipped line: '{line}' -> reason: {e}")

def count_by_priority(tickets):
    counts = {}
    for ticket in tickets:
        p = ticket["priority"]
        counts[p] = counts.get(p, 0) + 1
    return counts

if __name__ == "__main__":
    raw_lines = [
    "T001|high|login,auth",
    "T002|medium|billing",
    "T003|low|ui,cosmetic",
    "T004|urgent|payments",
    "T005|high|login,payments",
    "T006|medium",
    "T007|low|ui,auth,login",
]

valid_tickets = []

try:
    for ticket in clean_tickets(raw_lines):
        valid_tickets.append(ticket)
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print(f"Processed {len(valid_tickets)} valid tickets.")
finally:
    print("Triage pass complete.")

print(count_by_priority(valid_tickets))

target_tags = {"login", "payments"}
matching_ids = sorted([
    t["id"] for t in valid_tickets
    if t["tags"].intersection(target_tags)
])
print(matching_ids)