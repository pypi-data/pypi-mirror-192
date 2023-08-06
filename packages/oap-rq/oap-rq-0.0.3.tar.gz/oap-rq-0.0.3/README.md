# oap-rq



## Getting started

Simple Qmessiage Sender and Receiver using redis for python asyncio 

## installation

- pip install oap-rq
```
from oap_rq.q import QBus

q = QBus(redis, service="test", queue="customer-food")
resp = await q.send({"test": "me"})

print(resp)

```




