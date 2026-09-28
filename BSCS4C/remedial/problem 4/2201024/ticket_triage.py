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

logging.basicConfig(level=logging.INFO)

class TicketFormatError(Exception):
    pass

def log_call(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info(f"Calling {func.__name__}")

        try:
            return func(*args, **kwargs)

        finally:
            logging.info(f"{func.__name__} finished")

    return wrapper

@log_call
def parse_ticket_line(line):

    parts = line.split("|")

    if len(parts) != 3:

        raise TicketFormatError(
            f"expected 3 parts, got {len(parts)}"
        )

    ticket_id = parts[0].strip()
    priority = parts[1].strip().lower()
    tags_text = parts[2]

    valid_priorities = {"low", "medium", "high"}

    if priority not in valid_priorities:

        raise TicketFormatError(
            f"invalid priority: {priority}"
        )

    tags = {
        tag.strip().lower()
        for tag in tags_text.split(",")
    }

    return {
        "id": ticket_id,
        "priority": priority,
        "tags": tags,
    }


def clean_tickets(lines):

    for line in lines:
        try:
            ticket = parse_ticket_line(line)

        except TicketFormatError as error:

            print(
                f"Skipped line: {line!r} -> reason: {error}"
            )

        else:

            yield ticket
def count_by_priority(tickets):
    counts = {}

    for ticket in tickets:

        priority = ticket["priority"]

        counts[priority] = counts.get(priority, 0) + 1

    return counts


tickets = []

try:

    for ticket in clean_tickets(raw_lines):

        tickets.append(ticket)

except Exception as error:

    print(f"Unexpected error: {error}")

else:

    print(f"Processed {len(tickets)} valid tickets.")

finally:

    print("Triage pass complete.")
    priority_counts = count_by_priority(tickets)

print(priority_counts)

wanted_tags = {"login", "payments"}

matching_ids = [
    ticket["id"]
    for ticket in tickets
    if ticket["tags"] & wanted_tags
]
matching_ids = sorted(matching_ids)
print(matching_ids)