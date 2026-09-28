# Missing Value Decisions

The given pipeline has two reading columns wherein it treated differently on purpose, because they do not carry the same weight.

Temperature is the primary reading in this pipeline that exists to validate. If it becomes NaN, we don't know the actual temperature. Filling it with a guessed value could give a wrong result, especially for the alert check. So, we drop the row.

Humidityy is the second reading. West point still has valid temperature, so we don't want to remove the whole row just because humidity is missing. We fill the missing humidity with the column mean to keep the row usable.

These choices are not random. Temperature is more important in this pipeline, while humidity is secondary. That's why a missing temperature causes the row to be removed, while a missing humidity is filled.