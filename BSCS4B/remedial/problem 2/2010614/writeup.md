The core purpose of this data pipeline is to validate package weights 
so accurate routing decisions can be made. If a weight is entirely 
missing (`None`) or unparseable text (`heavy`), we cannot accurately 
calculate transportation costs or route the package safely. 

Filling these missing values with a guessed number (like a column mean 
or forward-fill) would result in physical routing errors, overloading 
delivery vehicles, or incorrect customer billing. Therefore, dropping 
invalid data entirely is the safest business decision.