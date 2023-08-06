# ConsentiumThingsPy

Developed by Debjyoti Chowdhury from ConsentiumInc

## Examples of How To Use (Buggy Alpha Version)

```python
from ConsentiumThingsPy import ThingsUpdate
import time

api_key = "Your send API key"

board = ThingsUpdate(key=api_key)

while True:
    # When You Are Done create sensor and info bucket
    sensor_val = [1, 2, 3, 4, 5, 6, 7]
    info_buff = ["a", "b", "c", "d", "e", "f", "g"]

    r = board.sendREST(sensor_val=sensor_val, info_buff=info_buff)
    print(r)
    time.sleep(5)
```
