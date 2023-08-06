import asyncio
import datetime
from dataclasses import asdict
from json import loads

from oap_rq import ack_queue_var, active_queue_var, client_addr_var, pending_queue_var
from oap_rq.logger import logger
from oap_rq.message import Message

TIME_DELTA_MIN = 5


class CommonVar:
    def __init__(self):
        self.redis = client_addr_var.get()
        self.ack_queue = ack_queue_var.get()
        self.stage = pending_queue_var.get()
        self.active_q = active_queue_var.get()


class Monitor(CommonVar):
    def has_expired(self, item):
        msg = Message(**loads(item))
        return msg if msg.expire_at <= datetime.datetime.utcnow() else None

    def extend_msg_duration(self, msg):
        return datetime.datetime.utcnow() + datetime.timedelta(minutes=TIME_DELTA_MIN)

    async def monitor_queue(self, evt):
        logger.info({"message": "Qeueue MONITOR", "status": "started"})
        TICK = 2
        while True:
            try:
                pipe = self.redis.pipeline()
                pipe.lrange(self.ack_queue, 0, -1)
                pipe.lrange(self.ack_queue, -2, -1)
                count, last_msgs = await pipe.execute()
                for last in last_msgs:
                    msg = self.has_expired(last)
                    if msg:
                        msg.expire_at = self.extend_msg_duration(msg)
                        item = await self.redis.lrem(self.ack_queue, 0, last)
                        if item:
                            logger.info(
                                {
                                    "message": "Queue MONITOR !!: expired item requeue",
                                    **loads(last),
                                }
                            )
                            await self.redis.lpush(self.active_q, msg.to_json_str())
                            logger.warn(
                                {"messge": "Items remaining", "total": len(count)}
                            )
                            TICK = 5

            finally:
                await asyncio.sleep(TICK)


class Receiver(Monitor):
    async def receive(self, worker):
        evt = asyncio.Event()
        task = asyncio.create_task(self.monitor_queue(evt))
        while True:
            data = await self.redis.rpoplpush(self.active_q, self.ack_queue)
            logger.info(
                {
                    "message": "waiting for data in the queue",
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
                        "message": "received ",
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
