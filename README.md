pyrc3563
=====

Python library and CLI tool for RC3563 battery impedance meter.

### Library usage

```python
from rc3563 import RC3563

rc = RC3563("/dev/ttyUSB0")
while True:
    print(rc.read())
```

### CLI tool

```shell
python -m cli /dev/ttyUSB0
# V: 4.118, R: 0.028483 # 28.483 mΩ
# V: 4.118, R: 0.028376 # 28.376 mΩ
# V: 4.118, R: 0.028264 # 28.264 mΩ
# V: 0.000, R: inf # overflow - nothing connected
```

## Credits

Based on the great work of [Maciej Grela](https://gist.github.com/enkiusz/e5e52e22e5d748645bf4d0ebe2c133dd).
