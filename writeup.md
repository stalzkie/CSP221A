Sensor Reading Cleaner

Missing-value decisions

For temperature, rows with missing values were removed because temperature is the primary sensor reading needed to determine the alert status.
For humidity, missing values were kept and replaced with the mean humidity because humidity is a secondary reading. This allows the station to remain in the cleaned dataset while still providing a usable value for the dry/normal flag.

What I learned

I learned how to use pandas to clean inconsistent station names, convert text readings into numeric values, remove duplicate stations, handle missing data, and create new columns based on conditions.

















    To pick up a draggable item, press the space bar.

    While dragging, use the arrow keys to move the item.
    
    Press space again to drop the item in its new position, or press escape to cancel.

