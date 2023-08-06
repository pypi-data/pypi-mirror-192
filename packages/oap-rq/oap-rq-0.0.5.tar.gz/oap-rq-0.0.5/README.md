# oap-rq



## Getting started

Simple Asyncio Queue message Sender and Receiver using redis
* Contains:
    * Sender
    * Receiver
    * Monitor

## Minimum Requirements
* python 3.8 or greater

## installation

- pip install oap-rq

# Usage 

```
from oap_rq.q import QBus

q = QBus(redis, service="test", queue="customer-food") # pass redis object 

```
# Sender
```
resp = await q.send({"test": "me"})
print(resp) #confirmation msg id
```
# Receiver

```
@q.consumer(name="foo-consumer")
async def process(event):
    async for e in event:
        print(e.data) # incoming data
        await e.ack()  # send msg ack 
        
```



