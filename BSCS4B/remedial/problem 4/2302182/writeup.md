I used a generator for "clean_signups()" because I wanted a program to be able to handle the signups one line at a time instead of creating another full list inside the function.
Using "yield" also makes sense in this case because valid signups can be passed out as they are processed.

So for my solution, I treated a line as malformed if it does not have exactly three parts that is separated by "|", or if the shift is not morning, afternoon, or evening.
When that happens, the program will raise "SignupFormatError", skip the bad line, and then continue with the rest.