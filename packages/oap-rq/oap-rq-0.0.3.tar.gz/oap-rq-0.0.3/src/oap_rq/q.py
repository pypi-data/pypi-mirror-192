import asyncio
import contextvars
import datetime
import uuid
from dataclasses import asdict, dataclass
from json import dumps, loads

from oap_rq.logger import logger

client_addr_var = contextvars.ContextVar("client_addr")
ack_queue_var = contextvars.ContextVar("consumer_ack")
pending_queue_var = contextvars.ContextVar("consumer_current")

INCR_MIN = 5


@dataclass
class Message:
    id: str
    data: dict
    queue: str
    expire_at: datetime.datetime

    async def ack(self):
        redis = client_addr_var.get()
        ack = ack_queue_var.get()
        consumer = pending_queue_var.get()
        pipe = redis.pipeline()
        pipe.lrem(ack, 0, self.to_json_str())
        pipe.hdel(consumer, self.id)
        await pipe.execute()

        logger.info(
            {
                "message": "sending ack to ack queue",
                "_id": self.id,
                "queue": self.queue,
                **asdict(self),
            }
        )
        logger.info({"message": "removed", "_id": self.id})

    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    def to_json_str(self):
        return dumps(asdict(self), default=self.default)


class RedisQueue:
    def __init__(self, redis, *, service="notify", queue="test"):
        self.redis = redis
        self.stage = f"{service}:{queue}:pending"
        self.ack_queue = f"{service}:{queue}:ack"
        self.active_q = f"{service}:{queue}"

    async def send(self, data, timeout=5):
        expire_at: datetime = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=timeout
        )
        msg = Message(
            id=uuid.uuid4().hex, data=data, queue=self.active_q, expire_at=expire_at
        )
        pipe = self.redis.pipeline()
        pipe.hset(self.stage, msg.id, msg.to_json_str())
        pipe.lpush(self.active_q, msg.to_json_str())
        await pipe.execute()
        logger.info({"message": {"id": msg.id, "status": "sent"}, **data})
        return msg.id

    def sync_send(self, data, timeout=5):
        """non async call"""
        expire_at: datetime = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=timeout
        )
        msg = Message(
            id=uuid.uuid4().hex, data=data, queue=self.active_q, expire_at=expire_at
        )
        pipe = self.redis.pipeline()
        pipe.hset(self.stage, msg.id, msg.to_json_str())
        pipe.lpush(self.active_q, msg.to_json_str())
        pipe.execute()
        return msg.id

    def has_expired(self, item):
        msg = Message(**loads(item))
        return msg if msg.expire_at <= datetime.datetime.utcnow() else None

    async def monitor_queue(self, evt):
        logger.info({"message": "Qeueue MONITOR", "status": "started"})
        TICK = 5
        while True:
            try:
                pipe = self.redis.pipeline()
                pipe.lrange(self.ack_queue, 0, -1)
                pipe.lrange(self.ack_queue, -2, -1)
                count, last_msgs = await pipe.execute()
                for last in last_msgs:
                    msg = self.has_expired(last)
                    if msg:
                        msg.expire_at = datetime.datetime.utcnow() + datetime.timedelta(
                            minutes=INCR_MIN
                        )
                        item = await self.redis.lrem(self.ack_queue, 0, last)
                        if item:
                            logger.info(
                                {
                                    "message": "Queue MONITOR !!: expired item requeue",
                                    **loads(last),
                                }
                            )
                            await self.redis.lpush(self.active_q, msg.to_json_str())
                            logger.warn("Items remaining", total=len(count))
                            TICK = 10

            finally:
                await asyncio.sleep(TICK)

    async def receive(self, worker):
        evt = asyncio.Event()
        client_addr_var.set(self.redis)
        ack_queue_var.set(self.ack_queue)
        pending_queue_var.set(self.stage)
        task = asyncio.create_task(self.monitor_queue(evt))
        while True:
            data = await self.redis.rpoplpush(self.active_q, self.ack_queue)
            logger.info(
                {
                    "message": "Current Active Qeue: waiting for data in the queue",
                    "worker": worker,
                }
            )
            if data:
                msg = Message(**loads(data))
                item = (
                    await self.redis.hget(self.stage, msg.id)
                    if await self.redis.hset(self.stage, msg.id, msg.to_json_str()) == 1
                    else msg.to_json_str()
                )
                logger.info(
                    {
                        "message": "Current Active Queue: ",
                        "queue": self.active_q,
                        "worker": worker,
                        **asdict(msg),
                    }
                )
                yield Message(**loads(item))
                evt.set()
            await asyncio.sleep(0.5)
            evt.clear()

        task.cancel()
        await task


class QBus:
    def __init__(self, redis, *, service="notify", queue="test"):
        self.redis = redis
        self.queue = RedisQueue(redis, service=service, queue=queue)

    async def send(self, data, timeout=5):
        return await self.queue.send(data, timeout)

    async def consume(self, name, worker):
        logger.info({"message": "Woker Starting ", "name": name, "worker_id": worker})
        async for f in self.queue.receive(worker):
            yield f

    def consumer(self, *, name: str, workers: int = 1):
        def _process(function):
            def decorated(*args, **kwargs):
                logger.info({"message": "Consumer", "name": name, "status": "started"})
                tasks = [
                    function(self.consume(name, worker), **kwargs)
                    for worker in range(1, workers + 1)
                ]

                async def inner():
                    task = [asyncio.create_task(f) for f in tasks]
                    return await asyncio.gather(*task)

                return inner()

            return decorated

        return _process
