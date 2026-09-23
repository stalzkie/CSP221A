I drop the station with missing temperature values because temperature is the primary reading in this pipeline to check, and the status is dependent on it. So I decided to drop entirely the station row name "East Ridge".

Humidity, I filled the missing value with the column mean, because humidity is secondary reading and the station temperature is still valid, dropping the row will be losing data over one missing field

Both are documented and with proper steps before doing the decisions and printed before and after the clean up, so the effect of each choice is visible