import logging
import functools

logging.basicConfig(level=logging.INFO)

raw_lines = [
    "T001|high|login,auth",
    "T002|medium|billing",
    "T003|low|ui,cosmetic",
    "T004|urgent|payments",
    "T005|high|login,payments",
    "T006|medium",
    "T007|low|ui,auth,login",
]

class TicketFormatError(Exception):
    pass

# logs each call, needed for R5
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"calling {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} finished")
        return result
    return wrapper


@log_calls
def parse_ticket_line(line):
    parts = line.split("|")

    if len(parts) != 3:
        raise TicketFormatError(f"expected 3 fields but got {len(parts)}: '{line}'")

    tid = parts[0].strip()
    prio = parts[1].strip().lower()

    if prio not in {"low", "medium", "high"}:
        raise TicketFormatError(f"bad priority '{parts[1].strip()}': '{line}'")

    tags = {t.strip().lower() for t in parts[2].split(",") if t.strip()}

    return {"id": tid, "priority": prio, "tags": tags}


def clean_tickets(lines):
    for line in lines:
        try:
            ticket = parse_ticket_line(line)
        except TicketFormatError as e:
            print(f"Skipped line: '{line}' -> reason: {e}")
        else:
            yield ticket


def count_by_priority(tickets):
    counts = {}
    for t in tickets:
        p = t["priority"]
        counts[p] = counts.get(p, 0) + 1
    return counts


tickets = []
try:
    for t in clean_tickets(raw_lines):
        tickets.append(t)
except TicketFormatError as e:
    print(f"failed: {e}")
else:
    print(f"Processed {len(tickets)} valid tickets.")
finally:
    print("Triage pass complete.")

print(count_by_priority(tickets))

wanted = {"login", "payments"}
found = []
for t in tickets:
    if t["tags"] & wanted:
        found.append(t["id"])
print(sorted(found))
