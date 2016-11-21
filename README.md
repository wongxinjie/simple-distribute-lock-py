### simple-distribute-lock-py
A very simple distribute lock implementation base on redis setnx.

#### install
```
git clone git@github.com:wongxinjie/simple-distribute-lock-py.git
cd simple-distribute-lock-py
python setup.py install
```

#### Getting Start
```
from redis import Redis
from distrolock import DistroLock

distrolock = DistroLock(conn=Redis(), lockname="name", lock_timeout=10)

lock = distrolock.acquire(timeout=5)
if lock:
    # do something here

distrolock.release()

# or use with statement
with DistroLock(conn=Redis(), lockname="with:name", lock_timeout) as distrolock:
    lock = distrolock.acquire()
    if lock:
        # do something here
```

