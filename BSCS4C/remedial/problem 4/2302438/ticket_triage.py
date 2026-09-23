from functools import wraps
import logging
# logging.basicConfig(level=logging.INFO)

raw_lines = [
    "T001|high|login,auth",
    "T002|medium|billing",
    "T003|low|ui,cosmetic",
    "T004|urgent|payments",
    "T005|high|  LOGIN  ,payments",
    "T006|medium",
    "T007|low|ui,auth,login         ",
]

class TicketFormatError(Exception):                                     # RULE 1
    # General error for format cases; contains different protocols depending on case via dict error_codes
    def __init__(self, error_code, *args):
        error_codes = {
            "PartError": f"!! LINE SKIPPED !! TicketFormatError 1: \"{args[1]}\" lacks 3 parts. ( {args[0]} ).",
            "PriorityError": f"!! LINE SKIPPED !! TicketFormatError 2: \"{args[1]}\" has an incorrect priority tag. ( \"{args[0][1]}\" )."
        }

        message = error_codes[error_code]
        super().__init__(message)

def log_parse(func):                                                    # RULE 5
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"parse operation attempt on {args[0]}")       
        r = func(*args, **kwargs)
        logging.info("parse operation attempt complete")
        return r
    return wrapper

@log_parse
def parse_ticket_line(raw_line):                                        # RULE 2
    e_line = raw_line
    raw_line = raw_line.split("|")

    if len(raw_line) != 3:
        raise TicketFormatError("PartError", raw_line, e_line)

    raw_line[1] = raw_line[1].lower()
    if raw_line[1] not in {"low", "medium", "high"}:
        raise TicketFormatError("PriorityError", raw_line, e_line)      # RULE 3

    raw_line[2] = {x.strip().lower() for x in raw_line[2].split(",")}   # RULE 4
    return raw_line

def clean_tickets(raw_lines, to_process):                               # RULE 6
    count = 0
    pcount = 0

    while count < to_process:
        try:                                                            # RULE 7
            raw_lines[count] = parse_ticket_line(raw_lines[count])
        except TicketFormatError as e:
            print(e)
            count += 1
            to_process += 1          
        else:
            dict = {
                "ticket_no": raw_lines[count][0],
                "priority": raw_lines[count][1],
                "tags": raw_lines[count][2]
            }
            count += 1
            pcount += 1
            yield dict
        finally:
            print(f"{pcount} valid tickets processed.")

    print(f"Triage pass complete.")

def count_by_priority(ticket_list):                                     # RULE 8
    counts = {
            "low": 0,
            "medium": 0,
            "high": 0
        }
    
    for x in ticket_list:
        priority = x.get("priority")

        counts[priority] = counts[priority] + 1

    return counts

def tag_search(ticket_list, search):
    return [x for x in ticket_list if bool(search & x["tags"])]


ticket_list = [x for x in clean_tickets(raw_lines, 5)]      # Cleans x amount of tickets from raw_lines, makes new list of dicts
print("FULL LIST:")
print(list(ticket_list))
print("\n")

counts = count_by_priority(ticket_list)                     # Creates a new dict, summing up priority tags
print("PRIORITY COUNT:")
print(counts)
print("\n")

search_login = tag_search(ticket_list, {"login"})           # Filters tickets by "login" tag
print("TAG LOOKUP: login")
print(search_login)
print("\n")

search_payments = tag_search(ticket_list, {"payments"})     # Filters tickets by "payments" tag
print("TAG LOOKUP: payments")
print(search_payments)
print("\n")

print("parse_ticket_line NAME:")                            # Prints name of parse_ticket_line function
print(parse_ticket_line.__name__)