To create my solution to the code, I went through each of the rules. Starting with the TicketFormatError, I created a function called parse_ticket_line, so as long as the line inst segmented in 3 parts and that the priorities are correct there will be no errors raised, if so the TicketFormatError will be raised on that line.

For the decorator part I wrapped the parse_ticket_line in log_calls wrapper which logs its name at the start and when the process has finished

For clean_tickets I had to make a generator instead of returning a list, this way once theres a bad line the process wont crash. So inside it I catch the TicketFormatError and use yield in the else part so that a ticket only gets yielded after parsing succeeded.

For the count_by_priority part, I created a counts dictionary and a loop over the tickets which adds 1 to the prioritys running total. So basically it checks how many tickets are in one priority.