# greyscale sensor

- Variations across sensor are small variations
- Take derivative across the points
    (difference of right/middle and left/middle)
    if difference is greater on one side, then we can do steering correction
    derivative automatically pulls out the mean

    how big do the differences have to be to trigger a turn?



### General flow (currently)
world -> GS -> interp -> controller -> car

### what we want
- sensor bus
- interpreter bus

world -> GS -> SENSOR BUS -> interp -> INTERPRETER BUS -> controller -> car
  |                             ^                               ^
  \> camera -> CAMERA BUS ------|                               |
  |                                                             |
  \> sonar -> SONAR BUS ----------------------------------------|


Write consumer/producer class that passes data for each sensor